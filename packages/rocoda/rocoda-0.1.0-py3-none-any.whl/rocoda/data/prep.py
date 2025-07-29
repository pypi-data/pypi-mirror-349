from rocoda.environments.robosuite import RobosuiteEnvironment
from h5py import File
from pathlib import Path
from tqdm.auto import tqdm
from typing import Union, Sequence, Mapping, Callable
import numpy as np
import json

# Dataset Preparation class

class DataPrep:

    def __init__(
            self,
            hdf5_path:Union[str, Path],
            env_type:str="robosuite",
            causal_objects:Sequence[str]=None):
        
        # Check if the file exists
        assert Path(hdf5_path).exists(), f"File {hdf5_path} does not exist"

        self.filepath = Path(hdf5_path)
        self.env_type = env_type

        with File(hdf5_path, "a") as filedata:

            if env_type == 'robosuite':
                
                if 'data' not in filedata:
                    raise AssertionError(f"File {hdf5_path.name} does not contain 'data'")

                # Create environment instance
                env_args = filedata['data'].attrs['env_args']
                env_args = json.loads(env_args)
                env_name = env_args['env_name'] # Name of robosuite env class
                env_kwargs = env_args['env_kwargs']
                self.env = RobosuiteEnvironment(env_name, env_kwargs)

            else:
                raise NotImplementedError(f"env_type {env_type} not supported")
            
            # If 'metadata' doesn't exist at root of the file, make it
            if 'metadata' not in filedata:
                filedata.create_group('metadata')
            else:
                if filedata['metadata'].attrs.get('causal_objects') and not causal_objects:
                    causal_objects = json.loads(filedata['metadata'].attrs['causal_objects'])

            self.robot_names = self.env.get_robot_names()
            self.object_names = self.env.get_object_names()

            default_causal_objects = self.robot_names + self.object_names

            if causal_objects:

                assert len(causal_objects) > 0, "causal_objects must be a non-empty list"
                assert set(causal_objects).issubset(default_causal_objects), f"{causal_objects} not subset of: {default_causal_objects}"
                self.causal_objects = causal_objects

            else:
                
                self.causal_objects = default_causal_objects
            
            # Save the metadata to the file
            filedata['metadata'].attrs['causal_objects'] = json.dumps(self.causal_objects, ensure_ascii=False)
            filedata['metadata'].attrs['env_type'] = env_type

    def __str__(self):
        return f"DataPrep(name={self.filepath.name})"
    
    def render_demo_state(
            self, 
            demo_idx:int, 
            state_idx:int, 
            camera_name:str="agentview"
            )->np.ndarray:
        
        with File(self.filepath, "r") as filedata:

            # Get the state
            demo_name = f"demo_{demo_idx}"
            states = filedata['data'][demo_name]['states']
            state = states[state_idx]

            # Reset the environment to this state
            self.env.reset_to({"states":state})

            # Render the image
            img = self.env.render(camera_name=camera_name)

            return img
    
    def apply_subtask_term_heuristic(
            self, 
            subtask_order:Sequence[str], 
            heuristic_func:Callable
            )->None:

        with File(self.filepath, "a") as filedata:

            # Iterate over all demos
            for demo in tqdm(filedata['data'], desc="labeling demo subtasks"):
                
                # Add a metadata group to this demo if not already present
                if 'metadata' not in filedata['data'][demo]:
                    filedata['data'][demo].create_group('metadata')
                
                states = filedata['data'][demo]['states']
                
                # Initialize empty list to hold subtask term signals
                signals = []

                for s_idx in range(states.shape[0]): # Iterate over all states in demo

                    # Set environment state
                    self.env.reset_to({"states" : states[s_idx]}) 

                    # Returns Sqeuence[Mapping[str,bool]] = [{subtask_name:bool, subtask_name:bool, ...}, ...]
                    # len(output) == len(robots); len(output[0]) == len(subtasks)
                    output = heuristic_func(self.env)

                    assert type(output) == dict, f"heuristic must return a dict of subtask signals, got {type(output)}"
                    assert set(output.keys()) == set(subtask_order), f"returned subtask names must equal subtask_order, got {output.keys()}"

                    signals.append(output)

                # Create empty list
                subtasks = np.zeros(states.shape[0], dtype=int)
                subtask_idx = 0
                for state_idx in range(len(states)):

                    cur_state = subtask_order[subtask_idx]
                    is_termed = signals[state_idx].get(cur_state, False)
                    if is_termed:
                        subtask_idx += 1
                    subtasks[state_idx] = subtask_idx

                # If "metadata" already exists at demo, delete it
                if 'metadata' in filedata['data'][demo]:
                    del filedata['data'][demo]['metadata']

                # Create a new metadata group
                filedata['data'][demo].create_group('metadata')

                # Add subtasks to metadata
                filedata['data'][demo]['metadata'].create_dataset(
                    'subtasks', 
                    data=subtasks,
                    compression='gzip',
                    compression_opts=9
                )
            
            # Save the subtask mappings to the filedata root metadata group as attribute
            filedata['metadata'].attrs['subtasks'] = json.dumps(subtask_order, ensure_ascii=False)

    def set_causal_groups(self, relations:Mapping[str, Sequence[Sequence[str]]])->None:
        '''
        Sets the per-subtask causality relations
        @param relations: {subtask_name: [(related_objects, ...),(...)], ... : ... }
        '''

        with File(self.filepath, "a") as filedata:

            # Get Subtask Order
            subtask_order = json.loads(filedata['metadata'].attrs['subtasks'])

            # Check that all subtask names are present
            assert set(list(relations.keys())) == set(subtask_order), \
                    "Missing Subtasks: set(relation.keys()) != set(subtasks)"

            # Check that all relation objects are in the causal objects
            for subtask, object_groups in relations.items():
                for object_group in object_groups:
                    for object_name in object_group:
                        assert object_name in self.causal_objects, \
                            f"object {object_name} not in causal_objects"

            # Save as metadata attribute
            filedata['metadata'].attrs['causal_groups'] = json.dumps(relations, ensure_ascii=False)