import argparse
import csv
import os
import pathlib

import cv2
import ffmpeg
import matplotlib.colors as mcolors
import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm
from pycocotools.coco import COCO

tqdm_bar_format = (
    "{desc}: {percentage:3.0f}% |{bar:30}| [{elapsed}<{remaining}, {rate_fmt}]"
)


def str2tuple(s):
    return tuple(map(int, s.split("x")))


def main():
    parser = argparse.ArgumentParser(
        description="Visualize MOT Challenge format with bounding boxes and trajectories."
    )
    parser.add_argument(
        "--mot-ch-file",
        "-m",
        type=str,
        required=True,
        help="Path to MOT Challenge format file.",
    )
    parser.add_argument(
        "--out-file",
        "-o",
        type=str,
        required=True,
        help="Path to output file without extension.",
    )
    parser.add_argument(
        "--image-dir",
        "-i",
        type=str,
        required=True,
        help="Path to directory containing images correspond to the MOT Challenge format file.",
    )
    parser.add_argument(
        "--resize",
        type=str2tuple,
        default=None,
        help="Resize images to the specified size. Example: 1920x1080",
    )
    parser.add_argument(
        "--mp4",
        action="store_true",
        help="If true, saves all frames as an MP4 video; if false, saves only the final frame as a PNG image.",
    )
    parser.add_argument(
        "--show-bbox",
        action="store_true",
        help="If true, shows bounding boxes in the visualization.",
    )
    parser.add_argument(
        "--coco_pred",
        type=str
    )
    parser.add_argument(
        "--coco_ann",
        type=str
    )
    args = parser.parse_args()

    assert (args.coco_pred != "") == (args.coco_ann != ""), "Both COCO predictions and COCO annotation must be provided!" 

    ch_file = args.mot_ch_file
    image_dir = args.image_dir
    out_file = args.out_file
    size = args.resize
    mp4 = args.mp4
    show_bbox = args.show_bbox

    sub = {}
    with open(ch_file, "r") as f:
        sub_csv = csv.reader(f)
        for line in sub_csv:
            frame_id = int(float(line[0]))
            if frame_id not in sub:
                sub[frame_id] = []
            sub[frame_id].append(
                {"track_id": int(float(line[1])), "bbox": list(map(float, line[2:6]))}
            )

    if args.coco_ann:
        coco = COCO(args.coco_ann)
        coco_pred = coco.loadRes(str(args.coco_pred))

        img_name2pred = {}
        for img_id in coco.imgs:
            img_info = coco.imgs[img_id]
            ann_ids = coco_pred.getAnnIds(imgIds=img_id)
            preds = coco_pred.loadAnns(ann_ids)
            img_name2pred[img_info["file_name"]] = preds

    else:
        img_name2pred = None


    visualize(sub, image_dir, out_file, size, mp4, show_bbox, img_name2pred)


def visualize(sub, image_dir, out_file, size=None, mp4=False, show_bbox=False, img_name2pred=None):
    image_paths = sorted([str(x) for x in pathlib.Path(image_dir).rglob("*.jpg")])

    colors = [mcolor2tuple(hex_color) for hex_color in mcolors.XKCD_COLORS.values()]

    bar = tqdm(
        total=len(image_paths), desc="Process Images", bar_format=tqdm_bar_format
    )

    drew_images = []
    trajectories = {}  # track_id -> [(x, y), ...]
    for i, image_path in enumerate(image_paths, 1):
        read_image = Image.open(image_path)
        img_copy = np.array(read_image).copy()
        draw = ImageDraw.Draw(read_image)
        annotations = sub.get(i, [])

        for annotation in annotations:
            track_id = annotation["track_id"]
            bbox = annotation["bbox"]

            color = colors[(track_id - 1) % len(colors)]

            if track_id not in trajectories:
                trajectories[track_id] = []
            trajectories[track_id].append(get_box_center(bbox))

            if show_bbox:
                draw.rectangle(
                    [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]],
                    outline=color,
                    width=5,
                )

        for _track_id, trajectory in trajectories.items():
            if len(trajectory) > 1:
                draw.line(
                    trajectory, fill=colors[(_track_id - 1) % len(colors)], width=5
                )

        if size is not None:
            read_image = read_image.resize(size)
        
        if img_name2pred:
            for pred in img_name2pred[str(pathlib.Path(*pathlib.Path(image_path).parts[-2:]))]:
                p1, p2 = (int(pred['bbox'][0]), int(pred['bbox'][1])), (int(pred['bbox'][0] + pred['bbox'][2]), int(pred['bbox'][1] + pred['bbox'][3]))
                img_copy = cv2.rectangle(img_copy, p1, p2, color=(0, 0, 255), thickness=1)
            read_image = np.array(read_image)
            read_image = np.concatenate([read_image, img_copy], axis=0)
            read_image = Image.fromarray(read_image)

        drew_images.append(read_image)

        bar.update(1)

    bar.close()

    save(drew_images, out_file, mp4)


def mcolor2tuple(mcolor):
    return tuple(int(mcolors.hex2color(mcolor)[i] * 255) for i in range(3))


def get_box_center(bbox):
    return (bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2)


def save(images, out_file, mp4):
    os.makedirs(pathlib.Path(out_file).parent, exist_ok=True)
    if mp4:
        file_with_ext = f"{out_file}.mp4"
        write_mp4(images, file_with_ext)
    else:
        file_with_ext = f"{out_file}.png"
        images[-1].save(file_with_ext)
    print(f"Saved to {file_with_ext}.")


def write_mp4(pil_images, file_name):
    import tempfile
    import subprocess

    bar = tqdm(
        total=len(pil_images) + 2, desc="Write to MP4  ", bar_format=tqdm_bar_format
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        for idx, pil_image in enumerate(pil_images):
            path = os.path.join(tmp_dir, f"frame_{idx:05d}.png")
            pil_image.save(path)
            bar.update(1)

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # overwrite without asking
            "-framerate", "10",
            "-i", os.path.join(tmp_dir, "frame_%05d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            file_name,
        ]

        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        bar.update(1)

    bar.update(1)
    bar.close()



if __name__ == "__main__":
    main()
