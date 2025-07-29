from rocoda.environments.robosuite import RobosuiteEnvironment
import torch, h5py, re, json
import networkx as nx
import numpy as np


class StateTemporalSplicing(torch.nn.Module):

    def __init__(self, dataset_path, p=1, intra_demo=False):
        with h5py.File(dataset_path, "r") as f:
            env_meta = json.loads(f["data"].attrs["env_args"])
            object_names = json.loads(f["metadata"].attrs["causal_objects"])
            causal_groups = json.loads(f["metadata"].attrs["causality"])
            self.causal_groups = []
            subtask_names = json.loads(f["metadata"].attrs["subtask_order"])
            self.num_robots = len(causal_groups)
            # Read causal groups from hdf5 file
            for robot in range(self.num_robots):
                self.causal_groups.append(
                    [causal_groups[robot][subtask] for subtask in subtask_names[robot]]
                )
            self.demo_ids = list(f["data"].keys())
            self.subtask_end_indices = {}  # episode_id -> robot -> phase_num
            self.subtask_start_indices = {}  # episode_id -> robot -> phase_num
            self.index_to_phase_num = {}  # episode_id -> timestep -> robot
            # Read subtask data from hdf5 file
            for episode_id in self.demo_ids:
                self.index_to_phase_num[episode_id] = np.array(
                    f[f"data/{episode_id}/metadata/subtasks"]
                ).transpose((1, 0))

                # fill in subtask_start_indices and subtask_end_indices
                self.subtask_end_indices[episode_id] = []
                self.subtask_start_indices[episode_id] = []
                episode_len = self.index_to_phase_num[episode_id].shape[0]
                for robot in range(self.num_robots):
                    self.subtask_end_indices[episode_id].append([])
                    self.subtask_start_indices[episode_id].append([])
                    for timestep in range(episode_len - 1):
                        if (
                            self.index_to_phase_num[episode_id][timestep, robot]
                            != self.index_to_phase_num[episode_id][timestep + 1, robot]
                        ):
                            self.subtask_end_indices[episode_id][robot].append(timestep)
                            self.subtask_start_indices[episode_id][robot].append(
                                timestep + 1
                            )
                    self.subtask_end_indices[episode_id][robot].append(episode_len - 1)
                    self.subtask_start_indices[episode_id][robot].insert(0, 0)

        self.curr_robot = 0
        env_name = env_meta["env_name"]
        env_name = env_name[:-3] if env_name[-2:] in ["D0", "D1", "D2"] else env_name
        self.env = RobosuiteEnvironment(env_name, env_meta["env_kwargs"])
        self.state_dim = self.env.get_state()["states"].shape[0]
        self.p = p
        self.intra_demo = intra_demo
        self.object_names = object_names
        self.object_name_to_index = {name: i for i, name in enumerate(object_names)}
        # indices of each object in flattened states array for splicing
        self.oject_metadata = self.env.get_object_addresses(object_names)
        self.dataset_path = dataset_path

    # Helper function to merge causal groups and create a NetworkX graph
    # Eg: causal groups [(cubeA, cubeB), (cubeB, cubeC)] will be merged to [(cubeA, cubeB, cubeC)]
    def generate_graph_from_causal_groups(self, causal_groups):
        groups = []
        for sub in causal_groups:
            merged = set(sub)
            to_remove = []
            for g in groups:
                if merged & g:  # If there's an intersection, merge
                    merged |= g
                    to_remove.append(g)
            for g in to_remove:
                groups.remove(g)
            groups.append(merged)

        # Step 2: Instantiate Graph
        G = nx.Graph()
        for group in groups:
            for node1 in group:
                for node2 in group:
                    if node1 != node2:
                        G.add_edge(node1, node2)
        return G

    def forward(self, data, episode_id, timestep):
        if np.random.rand() > self.p:
            self.curr_robot = (self.curr_robot + 1) % self.num_robots
            return data

        # get current phase for each robot and generate phase graph from merged causal groups
        _, qpos, action, pad = data
        phase_nums = self.index_to_phase_num[episode_id][timestep]
        causal_groups = []
        for robot in range(self.num_robots):
            causal_groups.extend(
                [self.causal_groups[robot][phase_num] for phase_num in phase_nums]
            )
        phase_graph = self.generate_graph_from_causal_groups(causal_groups)

        with h5py.File(self.dataset_path, "r") as f:
            curr_state = np.array([f"data/{episode_id}/states"][timestep][:])
            for obj_group in nx.connected_components(phase_graph):
                if self.intra_demo:
                    splice_episode = episode_id
                else:
                    splice_episode = np.random.choice(self.demo_ids)

                # choose index to splice from
                splice_phase_starts = [
                    self.subtask_start_indices[splice_episode][i][phase_nums[i]]
                    for i in range(len(phase_nums))
                ]
                splice_phase_ends = [
                    self.subtask_end_indices[splice_episode][i][phase_nums[i]]
                    for i in range(len(phase_nums))
                ]
                splice_timestep = np.random.randint(
                    np.max(splice_phase_starts), np.min(splice_phase_ends) + 1
                )

                # augment all but one robot
                if (
                    re.findall(r"robot\d+", " ".join(list(obj_group)))
                    and "robot" + str(self.curr_robot) not in obj_group
                ):
                    # get robot qpos
                    new_qpos = np.array(
                        f[f"data/{episode_id}/observations/qpos"][timestep]
                    )
                    qpos_start_index = self.curr_robot * len(qpos) // self.num_robots
                    qpos_end_index = (
                        (self.curr_robot + 1) * len(qpos) // self.num_robots
                    )
                    qpos[:qpos_start_index] = new_qpos[:qpos_start_index]
                    qpos[:qpos_end_index] = new_qpos[:qpos_end_index]

                    new_traj_len = new_qpos.shape[0]
                    action_len = new_traj_len - splice_timestep

                    # splice actions from all robots except curr_robot
                    action_start_index = (
                        self.curr_robot * action.shape[1] // self.num_robots
                    )
                    action_end_index = (
                        (self.curr_robot + 1) * action.shape[1] // self.num_robots
                    )

                    new_action = np.array(f[f"data/{episode_id}/action"][timestep])
                    action[:action_len, :action_start_index] = new_action[
                        :action_len, :action_start_index
                    ]
                    action[:action_len, action_end_index:] = new_action[
                        :action_len, action_end_index:
                    ]
                    action[action_len:, :] = 0
                    pad[:action_len] = 0
                    pad[action_len:] = 1
                    pad = pad.bool()

                # splice object states
                state_indices = []
                for obj in obj_group:
                    state_indices.extend(
                        self.oject_metadata[obj]["pos"]
                        + self.oject_metadata[obj]["vel"]
                    )
                splice_state = np.array(
                    f[f"data/{splice_episode}/states"][splice_timestep]
                )
                curr_state[state_indices] = splice_state[state_indices]
        # set env_state for rendering
        self.env.reset_to({"states": curr_state})
        self.curr_robot = (self.curr_robot + 1) % self.num_robots

        return (
            self.env.render(),
            qpos,
            action,
            pad,
        )  # TODO: check render format and correctness
