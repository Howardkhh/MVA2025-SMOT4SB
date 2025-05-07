import argparse
import json
import os
import os.path as osp
from PIL import Image

TRAIN_VAL_RATIO = (0.8, 0.2)
SRC_DIR = "datasets/SMOT4SB"
DEST_DIR = "OC_SORT/datasets/SMOT4SB"


def main():
    parser = argparse.ArgumentParser(
        description="Prepare the dataset to match the baseline code."
    )
    _ = parser.parse_args()

    os.makedirs(f"{DEST_DIR}/annotations", exist_ok=True)
    os.symlink(osp.abspath(f"{SRC_DIR}/private_test"), f"{DEST_DIR}/private_test")


    ann = {"images": [], "annotations": [], "categories": [{"id": 1, "name": "bird"}]}
    video_names = sorted(os.listdir(f"{SRC_DIR}/private_test"))
    
    img_id = 1
    video_id = 1

    for video_name in video_names:
        img_id_in_video = 1
        for img_name in sorted(os.listdir(f"{SRC_DIR}/private_test/{video_name}")):
            im = Image.open(f"{SRC_DIR}/private_test/{video_name}/{img_name}")
            width, height = im.size
            ann["images"].append(
                {
                    "file_name": f"{video_name}/{img_name}",
                    "id": img_id,
                    "frame_id": img_id_in_video,
                    "prev_image_id": img_id - 1 if img_id_in_video > 1 else -1,
                    "next_image_id": img_id + 1,
                    "video_id": video_id,
                    "height": height,
                    "width": width,
                }
            )
            img_id += 1
            img_id_in_video += 1
        ann["images"][-1]["next_image_id"] = -1
        video_id += 1


    with open(f"{DEST_DIR}/annotations/private_test.json", "w") as f:
        json.dump(ann, f)


if __name__ == "__main__":
    main()
