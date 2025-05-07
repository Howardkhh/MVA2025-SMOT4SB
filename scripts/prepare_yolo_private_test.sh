cd MVA2025-yolov9
cd JSON2YOLO && python general_json2yolo.py && cd ..
mkdir -p datasets/SMOT4SB && mv JSON2YOLO/SMOT4SB datasets/
cd datasets/SMOT4SB/images
ln -s ../../../../OC_SORT/datasets/SMOT4SB/private_test private_test
# copy COCO annotations
cd ..
cp -r ../../../OC_SORT/datasets/SMOT4SB/annotations/ .