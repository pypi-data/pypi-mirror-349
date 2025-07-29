from rocoda.environments.base import RocodaEnvironment
from typing import Sequence, Mapping
import numpy as np
import robosuite, mujoco


class RobosuiteEnvironment(RocodaEnvironment):

    def __init__(self, env_name, env_kwargs):

        super().__init__()

        # NOTE: ensure task class (env_name) is registered
        self.env = robosuite.make(env_name, **env_kwargs)

        # make sites invisible
        model = self.env.sim.model
        model.site_rgba[:, 3] = 0.0


    def get_underlying_env(self):
        return self.env

    def render(
            self, 
            camera_name:str = "agentview", 
            height:int = 256, 
            width:int = 256
            )->np.ndarray:

        #call mujoco render directly via env.sim
        img = self.env.sim.render(height=height, width=width, camera_name=camera_name)
        return img

    def reset(self):

        #reset the environment
        di = self.env.reset()
        
        # make sites invisible
        model = self.env.sim.model
        model.site_rgba[:, 3] = 0.0

        return self.get_observation(di)


    def reset_to(self, state:Mapping):

        if "model" in state:
            self.reset()
            xml = self.env.edit_model_xml(state["model"])
            self.env.reset_from_xml_string(xml)
            self.env.sim.reset()

        if "states" in state:
            self.env.sim.set_state_from_flattened(state["states"])
            self.env.sim.forward()

        return self.get_observation()
    

    def _get_real_depth_map(self, depth_map):
        """
        Reproduced from https://github.com/ARISE-Initiative/robosuite/blob/c57e282553a4f42378f2635b9a3cbc4afba270fd/robosuite/utils/camera_utils.py#L106
        since older versions of robosuite do not have this conversion from normalized depth values returned by MuJoCo
        to real depth values.
        """
        # Make sure that depth values are normalized
        assert np.all(depth_map >= 0.0) and np.all(depth_map <= 1.0)
        extent = self.env.sim.model.stat.extent
        far = self.env.sim.model.vis.map.zfar * extent
        near = self.env.sim.model.vis.map.znear * extent
        return near / (1.0 - depth_map * (1.0 - near / far))

    
    def get_observation(self, di=None):
        """
        Get current environment observation dictionary.

        Args:
            di (dict): current raw observation dictionary from robosuite to wrap and provide 
                as a dictionary. If not provided, will be queried from robosuite.
        """
        if di is None:
            di = self.env._get_observations(force_update=True)

        RGB_KEYS = {k for k in di if k.endswith("_image")}        
        DEPTH_KEYS = {k for k in di if k.endswith("_depth")}

        ret = {}
        for k in di:

            if k in RGB_KEYS:
                # by default images from mujoco are flipped in height
                ret[k] = di[k][::-1]

            elif k in DEPTH_KEYS:
                # by default depth images from mujoco are flipped in height
                ret[k] = di[k][::-1]
                if len(ret[k].shape) == 2:
                    ret[k] = ret[k][..., None] # (H, W, 1)
                assert len(ret[k].shape) == 3 
                # scale entries in depth map to correspond to real distance.
                ret[k] = self._get_real_depth_map(ret[k])

        # "object" key contains object information
        ret["object"] = np.array(di["object-state"])

        for robot in self.env.robots:
            # add all robot-arm-specific observations. Note the (k not in ret) check
            # ensures that we don't accidentally add robot wrist images a second time
            pf = robot.robot_model.naming_prefix
            for k in di:
                if k.startswith(pf) and (k not in ret) and not k.endswith("proprio-state"):
                    ret[k] = np.array(di[k])

        return ret

    def get_state(self)->Mapping:

        xml = self.env.sim.model.get_xml()  # model xml file
        state = np.array(self.env.sim.get_state().flatten())  # simulator state
        return dict(model=xml, states=state)

    def get_object_addresses(self, object_names:Sequence[str]):

        metadata = {}
        nq = self.env.sim.model.nq
        for name in object_names:
            for joint in self.env.sim.model.joint_names:
                if joint.startswith(name):
                    qpos = self.env.sim.model.get_joint_qpos_addr(joint)
                    if (type(qpos) is tuple):
                        qpos = list(range(qpos[0]+1, qpos[1]+1))
                    else:
                        qpos = [int(qpos+1)]
                    qvel = self.env.sim.model.get_joint_qvel_addr(joint)
                    if (type(qvel) is tuple):
                        qvel = list(range(qvel[0]+1+nq, qvel[1]+1+nq))
                    else:
                        qvel = [int(qvel+1+nq)]
                    metadata[name] = {
                        "pos": qpos,
                        "vel": qvel,
                    }
                    break
        return metadata

    def set_object_address(
            self, 
            object_name:str, 
            pos:float, 
            vel:float):

        new_state = self.get_state()["states"].copy()
        object_address = self.get_object_addresses([object_name])

        pos_idx_beg = object_address[object_name]["pos"][0] + 1
        pos_idx_end = object_address[object_name]["pos"][1] + 1
        new_state[pos_idx_beg:pos_idx_end] = pos

        cur_nq = self.env.sim.model.nq
        vel_idx_beg = object_address[object_name]["vel"][0] + 1 + cur_nq
        vel_idx_end = object_address[object_name]["vel"][1] + 1 + cur_nq
        new_state[vel_idx_beg:vel_idx_end] = vel

        self.reset_to(new_state)

    def get_object_names(self):
        return [x.name for x in self.env.model.mujoco_objects]

    def get_robot_names(self):
        robots = []
        for i in range(len(self.env.model.mujoco_robots)):
            robots += [f"robot{i}"]
        return robots
