# MVA 2025 Private Test Submission
## 0. Hardware Requirements
Our environment has been deployed into a Docker image that requires the NVIDIA Container Toolkit. The Docker image is based on CUDA 11.3, please make sure that your GPU driver version is at least 465.19.01.

It is recommended to execute our code using RTX 4090 with NVIDIA driver version `535.179`, as we have tested the following scripts and docker images with this setting.

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
└── private_test
    ├── 0001
    │   ├── 00001.jpg
    │   └── ...
    └── 0002
        ├── 00001.jpg
        └── ...
```

```bash
ln -s <absolute path to the SMOT4SB folder> ./datasets
```

### 1.3 Launching Docker Container
The docker container can be launched by:

```bash
docker run --rm	-i -t \
    -v $PWD:/root/MVA2025-SMOT4SB \
    -v $(readlink -f datasets/SMOT4SB):/root/MVA2025-SMOT4SB/datasets/SMOT4SB \
    --gpus all \
    --shm-size 32G \
    howardkhh/mva2025_elsalab_team1
```
After launching the Docker container, the working directory should be the `MVA2025-SMOT4SB` folder. 

**All of the commands below should be executed in `MVA2025-SMOT4SB` directory.**
The docker image is built with the `Dockerfile` within the root of our repository, and has been uploaded to the Dockerhub.

### 1.4 Install OC_SORT
```bash
cd OC_SORT
python3 setup.py develop
cd ..
```

## 2. Model Weights

Our model weights are too large to be uploaded to GitHub. Please download the pre-trained weights from Google Drive:

```bash
gdown --fuzzy https://drive.google.com/file/d/1QNC8WIx1YlDjHncqJViLYX4tnmYootWa/view?usp=sharing
unzip Weights.zip
```

A single folder named `Weights` should be downloaded to the root of our repository. 

**Important:** Please ensure that **all files** are fully downloaded (the progress bars should be at 100%). 

The size of the `final` folder should be 36 GB.
```bash
du -sh Weights
# output: 1.5G    Weights
```

## 3. Preprocess data
```bash
python scripts/prepare_private_test.py
bash scripts/prepare_yolo_private_test.sh
```

## 4. Folder Contents 
Please make sure that the files are in the following structure (only the most important files are listed):
```bash
MVA2025-SMOT4SB
├── MVA2025-WBF
├── MVA2025-yolov9
│   ├── datasets
│   │   └── SMOT4SB
│   │       ├── annotations
│   │       │   └── private_test.json
│   │       ├── images
│   │       │   └── private_test
│   │       │       ├── 0001
│   │       │       │   ├── 00001.jpg
│   │       │       │   └── ...
│   │       │       └── 0002
│   │       │           ├── 00001.jpg
│   │       │           └── ...
│   │       └── labels
│   └── ...
├── OC_SORT
├── TrackEval
├── Weights
│   ├── yolov9-e-mva-sahi-nwd-pos0.8-1024.pt
│   ├── yolov9-e-mva-sahi-nwd-pos0.8.pt
│   ├── yolov9-e-mva-sahi-nwd-stack_frame.pt
│   ├── yolov9-e-mva-sahi-nwd.pt
│   └── yolov9-e-mva-sahi.pt
├── assets
├── datasets
│   └── SMOT4SB -> <absolute path to the SMOT4SB folder>
│       └── private_test
│           ├── 0001
│           ├── 0002
│           └── ...
└── scripts
```

## 5. Inference Object Detection
```bash
bash scripts/inference_object_detection.sh
```

## 6. Ensemble Object Detection
```bash
cd MVA2025-WBF && \
python merge_multiple_coco.py --coco_ann ../MVA2025-yolov9/datasets/SMOT4SB/annotations/private_test.json --coco_pred ../MVA2025-yolov9/runs/private_test/yolov9-e-mva-sahi-nwd-pos0.8/yolov9-e-mva-sahi-nwd-pos0.8_predictions_no_nms.json ../MVA2025-yolov9/runs/private_test/yolov9-e-mva-sahi-nwd/yolov9-e-mva-sahi-nwd_predictions_no_nms.json ../MVA2025-yolov9/runs/private_test/yolov9-e-mva-sahi/yolov9-e-mva-sahi_predictions_no_nms.json ../MVA2025-yolov9/runs/private_test/yolov9-e-mva-sahi-nwd-stack_frame/yolov9-e-mva-sahi-nwd-stack_frame_predictions_no_nms.json ../MVA2025-yolov9/runs/private_test/yolov9-e-mva-sahi-nwd-pos0.8-1024/yolov9-e-mva-sahi-nwd-pos0.8-1024_predictions_no_nms.json --output_dir outputs_multiple_none,nwd,pos0.8,stack_frame,1024_nwd_pos0.8_1,1,1,1,2 --weights 1 1 1 1 2 && \
cd ..
```

## 7. Inference Tracking
```bash
bash scripts/predict_from_coco.sh --path OC_SORT/datasets/SMOT4SB/private_test --ann_path OC_SORT/datasets/SMOT4SB/annotations/private_test.json --pred_path MVA2025-WBF/outputs_multiple_none,nwd,pos0.8,stack_frame,1024_nwd_pos0.8_1,1,1,1,2/private_test/weighted_boxes_fusion_0.4_nwd.json --output_dir outputs/yolov9-sahi-none,nwd,pos0.8,stack_frame,1024_nwd_pos0.8_1,1,1,1,2_wbf-nwd0.4_tracker-nwd0.1 --use_nwd
```

## 8. Create Submission File
```bash
python scripts/create_submission.py -i outputs/yolov9-sahi-none,nwd,pos0.8,stack_frame,1024_nwd_pos0.8_1,1,1,1,2_wbf-nwd0.4_tracker-nwd0.1/predictions/private_test
```

# The submission file will be saved in `yyyy-mm-dd_hh-mm-ss.zip`.

# Acknowledgement
This repository is modified from [IIM-TTIJ/MVA2025-SMOT4SB](https://github.com/IIM-TTIJ/MVA2025-SMOT4SB.git), [WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9.git), and [ZFTurbo/Weighted-Boxes-Fusion](https://github.com/ZFTurbo/Weighted-Boxes-Fusion.git).
