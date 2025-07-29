from rocoda.environments.robosuite import RobosuiteEnvironment
from tqdm.auto import tqdm
import numpy as np
import h5py, json

# Implement Causal State-Splicing Augmentation
# TODO implement bimanual splicing
# TODO implement online splicing

def augment(
        filepath:str, 
        num_new_episodes:int=None, 
        across_demos:bool=True,
        seed:int=0):
    
    with h5py.File(filepath, "a") as data:

        env_type = data['metadata'].attrs.get('env_type')
        
        if env_type is None:
            raise AssertionError(f"File {filepath} does not contain 'env_type'")
        
        if env_type != 'robosuite':
            raise NotImplementedError(f"env_type {env_type} not supported")
        
        else:
            #initialize environment
            env_args = data['data'].attrs['env_args']
            env_args = json.loads(env_args)
            env_name = env_args['env_name']
            env_kwargs = env_args['env_kwargs']
            env = RobosuiteEnvironment(env_name, env_kwargs)

        def get_attr(name):
            return json.loads(data["metadata"].attrs[name])
        
        # get various saved attributes
        robot_names = env.get_robot_names()
        causal_objects = get_attr("causal_objects")
        causal_groups = get_attr("causal_groups")
        subtasks = get_attr("subtasks")
        demo_ids = list(data["data"].keys())
        demo_ids = [d for d in demo_ids if not "rocoda" in d]
        obs_keys = list(data["data"][demo_ids[0]]["obs"].keys())
        obs_keys = [k for k in obs_keys if k in env.get_observation().keys()]
        if num_new_episodes is None:
            num_new_episodes = len(demo_ids)
        obj_meta = env.get_object_addresses(causal_objects)

        # set numpy random seed
        np.random.seed(seed)

        # create each new episode
        for new_ep in tqdm(range(num_new_episodes)):

            # create a new episode ID, delete if it exists
            new_ep_id = f"demo_rocoda_{new_ep}"
            if new_ep_id in data['data']:
                del data['data'][new_ep_id]
            data.create_group(f"data/{new_ep_id}")
            
            # randomly select a source episode
            source_ep = np.random.choice(demo_ids)

            # copy old actions to new episode
            data.copy(
                data[f"data/{source_ep}/actions"],
                data[f"data/{new_ep_id}"],
                "actions",
            )

            # copy old rewards to new episode
            data.copy(
                data[f"data/{source_ep}/rewards"],
                data[f"data/{new_ep_id}"],
                "rewards",
            )

            # copy old dones to new episode
            data.copy(
                data[f"data/{source_ep}/dones"],
                data[f"data/{new_ep_id}"],
                "dones",
            )

            # Create new episode states

            new_ep_states = np.array(data[f"data/{source_ep}/states"])
            subtask_inds = np.array(data[f"data/{source_ep}/metadata/subtasks"])

            num_steps = new_ep_states.shape[0]
            for ts in range(num_steps): #iterate over timesteps

                cur_subtask_id = subtask_inds[ts]
                cur_subtask_name = subtasks[cur_subtask_id]
                cur_groups = causal_groups[cur_subtask_name]
                all_listed_objs = set()
                for group in cur_groups:
                    for obj in group:
                        all_listed_objs.add(obj)
                unlisted_objs = set(causal_objects) - all_listed_objs
                for obj in unlisted_objs:
                    cur_groups.append([obj])

                for group in cur_groups: #iterate over groups
                
                    # don't augment groups containing robots
                    if any(obj in robot_names for obj in group):
                        continue

                    # select a splice episode
                    if across_demos:
                        splice_episode = np.random.choice(demo_ids)
                    else:
                        splice_episode = source_ep

                    # get indices of the subtask in splice episode
                    splice_subtask_inds = np.array(
                        data[f"data/{splice_episode}/metadata/subtasks"]
                    )

                    # get ts of splice episode with same subtask
                    splice_ts_options = np.where(splice_subtask_inds == cur_subtask_id)[0]

                    # randomly select a splice timestep
                    splice_ts = np.random.choice(splice_ts_options)

                    # get the states of the splice episode
                    splice_states = np.array(data[f"data/{splice_episode}/states"])

                    # get indices within a state splice corresponding to all obj within cur group
                    obj_state_inds = []
                    for obj in group:
                        pos_inds = obj_meta[obj]["pos"]
                        vel_inds = obj_meta[obj]["vel"]
                        obj_state_inds.extend(pos_inds + vel_inds)

                    # splice the states
                    new_ep_states[ts, obj_state_inds] = splice_states[
                        splice_ts, obj_state_inds
                    ]

            # save new episode states
            data.create_dataset(
                f"data/{new_ep_id}/states",
                data=new_ep_states,
                compression="gzip",
                compression_opts=9,
            )

            # Create new episode observations
            new_ep_obs = {k:[] for k in obs_keys}
            for ts in range(num_steps):
                obs = env.reset_to({"states": new_ep_states[ts]})
                for k in obs_keys:
                    val = np.expand_dims(obs[k], axis=0)
                    new_ep_obs[k].append(val)
            new_ep_obs = {k: np.concatenate(v, axis=0) for k, v in new_ep_obs.items()}

            # save new episode observations
            data.create_group(f"data/{new_ep_id}/obs")
            for k in obs_keys:
                data.create_dataset(
                    f"data/{new_ep_id}/obs/{k}",
                    data=new_ep_obs[k],
                    compression="gzip",
                    compression_opts=9,
                )

def augment_online(
        filepath:str, 
        num_new_episodes:int=None, 
        across_demos:bool=True,
        seed:int=0):
    
    raise NotImplementedError("Online splicing not implemented yet")