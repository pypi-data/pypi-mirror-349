# ROCODA Alpha 0.1

To install
```bash
git clone git@github.com:pairlab/rocoda.git
cd rocoda
conda create -n rocoda python=3.10
conda activate rocoda
pip install -r requirements.txt
pip install -e .
```

Additionally, to pull `example/stack_three.hdf5`, you will need to install Git LFS (Large File Storage).
On Ubuntu, run

```bash
sudo apt update
sudo apt install git-lfs
git lfs install
git lfs pull
```