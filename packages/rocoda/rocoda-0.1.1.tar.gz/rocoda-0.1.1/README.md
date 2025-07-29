# RoCoDA Alpha 0.1
## Counterfactual Data Augmentation for Data-Efficient Robot Learning from Demonstrations

Project Description for RoCoDA [here](https://rocoda.github.io/)

To install:

via `uv` (recommended):

```bash
git clone github.com/pairlab/rocoda
cd rocoda
uv venv
source .venv/bin/activate
uv pip install -e .
```

Additionally, to pull `example/stack_three.hdf5` and `datasets/*`, you will need to install Git LFS (Large File Storage).

On Ubuntu, run

```bash
sudo apt update
sudo apt install git-lfs
git lfs install
git lfs pull
```