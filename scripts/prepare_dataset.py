import argparse
import json
import os
import os.path as osp
from PIL import Image

TRAIN_VAL_RATIO = (0.8, 0.2)
SRC_DIR = "datasets/SMOT4SB"
DEST_DIR = "OC_SORT/datasets/SMOT4SB"


def filter_by_video_ids(anno, target_video_names):
    video_ids = {
        video["id"] for video in anno["videos"] if video["name"] in target_video_names
    }
    images = [img for img in anno["images"] if img["video_id"] in video_ids]
    image_ids = {img["id"] for img in images}
    annotations = [ann for ann in anno["annotations"] if ann["image_id"] in image_ids]
    videos = [video for video in anno["videos"] if video["id"] in video_ids]

    return {
        "images": images,
        "annotations": annotations,
        "videos": videos,
        "categories": anno["categories"],
    }


def split_train_dir(train_video_names, val_video_names):
    os.makedirs(f"{DEST_DIR}/train", exist_ok=True)
    os.makedirs(f"{DEST_DIR}/val", exist_ok=True)

    for video_name in train_video_names:
        os.symlink(
            osp.abspath(f"{SRC_DIR}/train/{video_name}"),
            f"{DEST_DIR}/train/{video_name}",
        )

    for video_name in val_video_names:
        os.symlink(
            osp.abspath(f"{SRC_DIR}/train/{video_name}"), f"{DEST_DIR}/val/{video_name}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Prepare the dataset to match the baseline code."
    )
    _ = parser.parse_args()

    with open(f"{SRC_DIR}/annotations/train.json", "r") as f:
        train_anno = json.load(f)

    videos = train_anno["videos"]
    # train_video_names = [
    #     video["name"] for video in videos[: int(len(videos) * TRAIN_VAL_RATIO[0])]
    # ]
    # val_video_names = [
    #     video["name"] for video in videos[int(len(videos) * TRAIN_VAL_RATIO[0]) :]
    # ]
    train_video_names = ["0001",  "0004",  "0007",  "0010",  "0013",  "0016",  "0019",  "0022",  "0025",  "0028",  "0031",  "0034",  "0037",  "0040",  "0043",  "0046",  "0049",  "0057",  "0061",  "0065",  "0069",  "0077",  "0081",  "0084",  "0089",  "0096",
        "0002",  "0005",  "0008",  "0011",  "0014",  "0017",  "0020",  "0023",  "0026",  "0029",  "0032",  "0035",  "0038",  "0041",  "0044",  "0047",  "0050",  "0059",  "0063",  "0067",  "0071",  "0078",  "0082",  "0085",  "0090",
        "0003",  "0006",  "0009",  "0012",  "0015",  "0018",  "0021",  "0024",  "0027",  "0030",  "0033",  "0036",  "0039",  "0042",  "0045",  "0048",  "0051",  "0060",  "0064",  "0068",  "0073",  "0080",  "0083",  "0087",  "0091"
    ]
    train_video_names.extend(["0097", "0098", "0099", "0100", "0101", "0102", "0103", "0104", "0105", "0106", "0107", "0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115", "0116", "0117", "0118", "0119", "0120", "0121", "0122"])
    val_video_names = ["0052",  "0053",  "0054",  "0055",  "0056",  "0058",  "0062",  "0066",  "0070",  "0072",  "0074",  "0075",  "0076",  "0079",  "0086",  "0088",  "0092",  "0093",  "0094",  "0095"
    ]
    val_video_names.extend(["0123", "0124", "0125", "0126", "0127", "0128"])

    splitted_train_anno = filter_by_video_ids(train_anno, train_video_names)
    splitted_val_anno = filter_by_video_ids(train_anno, val_video_names)

    os.makedirs(f"{DEST_DIR}", exist_ok=True)
    os.symlink(osp.abspath(f"{SRC_DIR}/pub_test"), f"{DEST_DIR}/pub_test")
    split_train_dir(train_video_names, val_video_names)

    os.makedirs(f"{DEST_DIR}/annotations", exist_ok=True)
    with open(f"{DEST_DIR}/annotations/train.json", "w") as f:
        json.dump(splitted_train_anno, f)
    with open(f"{DEST_DIR}/annotations/val.json", "w") as f:
        json.dump(splitted_val_anno, f)


    ann = {"images": [], "annotations": [], "categories": [{"id": 1, "name": "bird"}]}
    video_names = sorted(os.listdir(f"{SRC_DIR}/pub_test"))
    
    img_id = 1
    video_id = 1

    for video_name in video_names:
        img_id_in_video = 1
        for img_name in sorted(os.listdir(f"{SRC_DIR}/pub_test/{video_name}")):
            im = Image.open(f"{SRC_DIR}/pub_test/{video_name}/{img_name}")
            width, height = im.size
            if width != 3840 or height != 2160: print(f"{video_name}/{img_name}")
            ann["images"].append(
                {
                    "file_name": f"{video_name}/{img_name}",
                    "id": img_id,
                    "frame_id": img_id_in_video,
                    "prev_image_id": img_id - 1 if img_id > 1 else -1,
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


    with open(f"{DEST_DIR}/annotations/pub_test.json", "w") as f:
        json.dump(ann, f)


if __name__ == "__main__":
    main()
