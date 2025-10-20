import argparse
import os
import sys
import json
from prime_math import compute_score
from constraint_registry import INSTRUCTION_DICT

parser = argparse.ArgumentParser()
parser.add_argument(
    '--hypothesis_path', 
    type=str,
    default="/content/drive/MyDrive/SafeDPO/IFEval_outputs/"
)
parser.add_argument(
    '--data_path', 
    type=str,
    default="/content/drive/MyDrive/MathIF/data/"
)
parser.add_argument("--delimiter", type=str, default="</think>")
args = parser.parse_args()


def test_instruction_following_strict(
    instruction_id_list,
    response,
    parameters,
    prompt,
):
    """Tests response to see if instructions are followed."""

    is_following_list = []
    for index, instruction_id in enumerate(instruction_id_list):
        try:
            instruction_cls = INSTRUCTION_DICT[instruction_id]
        except:
            import pdb
            pdb.set_trace()
        instruction = instruction_cls(instruction_id)

        # Remove None values from kwargs to avoid unexpected keyword argument errors in build_description method.  
        if parameters[index]:
            kwargs = {n: p for n, p in parameters[index].items() if p}
        else:
            kwargs = {}
        instruction.build_description(**kwargs)
        args_dict = instruction.get_constraint_args()
        if args_dict and "prompt" in args_dict:
            instruction.build_description(prompt=prompt)
        try:
            if response.strip() and instruction.check_following(response):
                is_following_list.append(True)
            else:
                is_following_list.append(False)
        except:
            import pdb
            pdb.set_trace()

    return is_following_list


strict = []
loose = []
correct = []


# ✅ 这里改动：自动遍历网盘下所有生成文件
from glob import glob

hypothesis_files = sorted(glob(os.path.join(args.hypothesis_path, "*.jsonl")))

if not hypothesis_files:
    print(f"❌ No hypothesis files found in {args.hypothesis_path}")
    sys.exit(0)

for hyp_file in hypothesis_files:
    # 根据文件名自动推断 dataset 文件
    filename = os.path.basename(hyp_file)
    # 提取 dataset_constraint
    if "_noconstraint" in filename:
        dataset_constraint = filename.split("_")[-5:-3]
    else:
        dataset_constraint = filename.split("_")[-4:-2]
    dataset_constraint = "_".join(dataset_constraint)
    data_file = os.path.join(args.data_path, f"{dataset_constraint}.jsonl")

    if not os.path.exists(data_file):
        print(f"⚠️ Missing data file for {dataset_constraint}, skipping...")
        continue

    print(f"🔹 Evaluating {filename} ...")

    for line1, line2 in zip(open(hyp_file).readlines(), open(data_file).readlines()):
        try:
            hypothesis = json.loads(line1)["output"]
        except:
            hypothesis = json.loads(line1)["response"]
        if isinstance(hypothesis, list):
            hypothesis = hypothesis[0]
        has_end_think = '</think>' in hypothesis
        has_start_think = '<think>' in hypothesis

        think = hypothesis
        if has_end_think:
            think = think.split("</think>")[0]
        if '<think>' in think:
            think = think.split('<think>')[1]

        if '<think>' in hypothesis:
            hypothesis = hypothesis.split('<think>')[1]
        if '</think>' in hypothesis:
            hypothesis = hypothesis.split('</think>')[1]
        if '<answer>' in hypothesis:
            hypothesis = hypothesis.split('<answer>')[1]
        if '</answer>' in hypothesis:
            hypothesis = hypothesis.split('</answer>')[0] 

        data = json.loads(line2)
        if not ("noconstraint" in hyp_file):
            is_follow_list = test_instruction_following_strict(
                data["constraint_name"],
                hypothesis,
                data["constraint_args"],
                data["question"],
            )
            strict.append(all(is_follow_list))
            loose.append(sum(is_follow_list)/len(is_follow_list))
        else:
            strict.append(1)
            loose.append(1)

        if compute_score(hypothesis, data['answer'])[0]:
            correct.append(1)
        else:
            correct.append(0)

print("==== Evaluation Results ====")
print("Strict follow:", sum(strict)/len(strict))
print("Loose follow:", sum(loose)/len(loose))
print("Correct:", sum(correct)/len(correct))
