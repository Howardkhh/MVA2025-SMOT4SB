#!/bin/bash
set -e

cd MVA2025-yolov9

python val_dual.py --data data/mva2025-private_test.yaml --img 640 --batch 1 --conf 0.001 --iou 0.6 --device 0 --weights ../Weights/yolov9-e-mva-sahi.pt --save-json --name yolov9-e-mva-sahi --sahi sahi --task test --project runs/private_test

python val_dual.py --data data/mva2025-private_test.yaml --img 640 --batch 1 --conf 0.001 --iou 0.6 --device 0 --weights ../Weights/yolov9-e-mva-sahi-nwd.pt --save-json --name yolov9-e-mva-sahi-nwd --sahi sahi --task test --project runs/private_test

python val_dual.py --data data/mva2025-private_test.yaml --img 640 --batch 1 --conf 0.001 --iou 0.6 --device 0 --weights ../Weights/yolov9-e-mva-sahi-nwd-pos0.8.pt --save-json --name yolov9-e-mva-sahi-nwd-pos0.8 --sahi sahi --task test --project runs/private_test

python val_dual.py --data data/mva2025-private_test.yaml --img 640 --batch 32 --conf 0.001 --iou 0.6 --device 0 --weights ../Weights/yolov9-e-mva-sahi-nwd-stack_frame.pt --save-json --name yolov9-e-mva-sahi-nwd-stack_frame --sahi sahi --stack_frame -3 -1 0 1 3 --task test --project runs/private_test

python val_dual.py --data data/mva2025-private_test.yaml --img 640 --batch 1 --conf 0.001 --iou 0.6 --device 0 --weights ../Weights/yolov9-e-mva-sahi-nwd-pos0.8-1024.pt --save-json --name yolov9-e-mva-sahi-nwd-pos0.8-1024 --sahi sahi --task test --project runs/private_test