from rocoda.environments.base import RocodaEnvironment

class IssacSimEnvironment(RocodaEnvironment):

    def __init__(self, env_name, env_kwargs):
        raise NotImplementedError
    
    def step(self, action):
        raise NotImplementedError
    
    def render(self, camera_name):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    def reset_to(self, state):
        raise NotImplementedError
    
    def get_state(self):
        raise NotImplementedError
    
    def get_object_addresses(self, objects):
        raise NotImplementedError
    
    def set_object_address(self, object_name, pos, vel):
        raise NotImplementedError
    
    def get_object_names(self):
        raise NotImplementedError
    
    def get_robot_names(self):
        raise NotImplementedError