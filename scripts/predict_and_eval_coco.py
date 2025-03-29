import argparse
import os

parser = argparse.ArgumentParser(description='Predict and evaluate on COCO object detection resutls')
parser.add_argument('--path', type=str, required=True, help='path to the videos')
parser.add_argument('--ann_path', type=str, required=True, help='path to coco annotation file')
parser.add_argument('--pred_path', type=str, required=True, help='path to coco prediction file')
parser.add_argument('--output_dir', type=str, required=True, help='output directory')
parser.add_argument('--split', type=str, default='val', choices=['val', 'train'], help='split to evaluate on')
args = parser.parse_args()

if os.system(f"bash scripts/predict_from_coco.sh --path {args.path} --ann_path {args.ann_path} --pred_path {args.pred_path} --output_dir {args.output_dir}"):
    print("Error running predict_from_coco.sh")
    exit(1)
if os.system(f"python scripts/cp_preds_for_eval.py -i {args.output_dir}/predictions/{args.split}/ -o eval_inputs"):
    print("Error running cp_preds_for_eval.py")
    exit(1)
if os.system(f"python scripts/oc_sort_ann_to_mot_ch.py -i OC_SORT/datasets/SMOT4SB/annotations/{args.split}.json -o eval_inputs"):
    print("Error running oc_sort_ann_to_mot_ch.py")
    exit(1)
if os.system(f"python TrackEval/scripts/run_smot4sb_challenge.py eval_inputs eval_outputs {args.split} --metric-smot4sb"):
    print("Error running run_smot4sb_challenge.py")
    exit(1)