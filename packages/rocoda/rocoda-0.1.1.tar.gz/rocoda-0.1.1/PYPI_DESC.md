# RoCoDA Alpha 0.1
## Counterfactual Data Augmentation for Data-Efficient Robot Learning from Demonstrations

Project Description for RoCoDA [here](https://rocoda.github.io/)

To install via `uv` (recommend)

```bash
uv venv
source .venv/bin/activate
uv pip install rocoda
```

# Examples

Instantiate DataPrep Object:


```python
#NOTE: all data preparation is done in-place on disk
from rocoda.data.prep import DataPrep
from task import StackThree_D0 #registers the task

data = DataPrep(
    hdf5_path="stack_three.hdf5", 
    env_type="robosuite")
```

Render a Frame:

```python
from PIL import Image

img = data.render_demo_state(0, 10, camera_name="agentview")
img = Image.fromarray(img)
img = img.transpose(Image.FLIP_TOP_BOTTOM)
display(img)
```

Define Subtask Boundaries via Heuristic:

```python
from rocoda.environments.robosuite import RobosuiteEnvironment
from typing import Mapping

# Define subtask heuristic for StackThree
def heuristic(rocoda_env:RobosuiteEnvironment)->Mapping[str,bool]:

    env = rocoda_env.get_underlying_env() #gets the robosuite env

    signals = {
        "grasp_1": False,
        "stack_1": False,
        "grasp_2": False,
        "stack_2": False
    }

    signals["grasp_1"] = env._check_grasp(gripper=env.robots[0].gripper, object_geoms=env.cubeA)

    signals["stack_1"] = env._check_cubeA_stacked()

    signals["grasp_2"] = env._check_grasp(gripper=env.robots[0].gripper, object_geoms=env.cubeC)

    return signals
            
# Apply subtask termination heuristic
data.apply_subtask_term_heuristic( ["grasp_1","stack_1","grasp_2","stack_2"], heuristic )
```

Define the Causal Groups:

```python
# Expects [{subtask_name: {object_name: [object_name, ...]}}] * num_robots

causality = {
    "grasp_1": [("robot0", "cubeA")],
    "stack_1": [("robot0", "cubeA", "cubeB")],
    "grasp_2": [("robot0", "cubeC"),("cubeA","cubeB")],
    "stack_2": [("robot0", "cubeA", "cubeB", "cubeC")]
}

# Set the causality groups for the dataset
data.set_causal_groups(causality)
```

Run Causal Augmentation:

```python
from rocoda.augments import causal

causal.augment(
    filepath="stack_three.hdf5",
    num_new_episodes=10,
    across_demos=True)
```