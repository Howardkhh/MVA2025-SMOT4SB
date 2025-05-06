# MVA 2025 Private Test Submission
## 0. Hardware Requirements
Our environment has been deployed into a Docker image that requires the NVIDIA Container Toolkit. The Docker image is based on CUDA 11.3, please make sure that your GPU driver version is at least 465.19.01.

It is recommended to execute our code using RTX 4090, as we have tested the following scripts and docker images on this device.

## 1. Environment Setup
### 1.1 Clone this repository:
```bash
git clone --recurse-submodules https://github.com/Howardkhh/MVA2025-SMOT4SB.git
cd MVA2025-SMOT4SB
```

### 1.2 Preparing Private Test Data
Before launching the Docker container, ensure that the data folder is linked to our repository. The data folder should contain the private test folder named `SMOT4SB`. Inside this folder, the private test images should be placed in the `private_test` folder.

```bash
SMOT4SB
├── private_test
│   ├── 0001
│       ├── 00001.jpg
│       └── ...
│   └── 0002
│       ├── 00001.jpg
│       └── ...
└── ...
```

```bash
ln -s <absolute path to the SMOT4SB folder> ./datasets
```

### 1.3 Launching Docker Container
The docker container can be launched by:

```bash
docker run --rm	-i -t \
    -v $(PWD):/root/MVA2025-SMOT4SB \
    -v $(shell readlink -f datasets/SMOT4SB):/root/MVA2025-SMOT4SB/datasets/SMOT4SB \
    --gpus all \
    --shm-size 32G \
    howardkhh/mva2025_elsalab_team1
```
After launching the Docker container, the working directory should be the `MVA2025-SMOT4SB` folder. 

**All of the commands below should be executed in `MVA2025-SMOT4SB` directory.**
```
The docker image is built with the `Dockerfile` within the root of our repository, and has been uploaded to the Dockerhub.


# Acknowledgement
This repository is modified from [IIM-TTIJ/MVA2025-SMOT4SB](https://github.com/IIM-TTIJ/MVA2025-SMOT4SB.git), [WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9.git), and [ZFTurbo/Weighted-Boxes-Fusion](https://github.com/ZFTurbo/Weighted-Boxes-Fusion.git).