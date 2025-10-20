import argparse
import os
import sys
import json
from prime_math import compute_score
from constraint_registry import INSTRUCTION_DICT

parser = argparse.ArgumentParser()
# ✅ 只修改 hypothesis_path 的默认值为你的网盘目录
parser.add_argument(
    '--hypothesis_path',
    type=str,
    default="/content/drive/MyDrive/SafeDPO/IFEval_outputs/"
)
parser.add_argument('--data_path', type=str)  # 不改这里
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

# ✅ 新增：支持 hypothesis_path 是目录时自动遍历所有 .jsonl
from glob import glob

if os.path.isdir(args.hypothesis_path):
    hypothesis_files = sorted(glob(os.path.join(args.hypothesis_path, "*.jsonl")))
else:
    hypothesis_files = [args.hypothesis_path]


for line1,line2 in zip(open(args.hypothesis_path).readlines(), open(args.data_path).readlines()):
    record = json.loads(line1)
    # ✅ 自动兼容各种字段名
    hypothesis = (
        record.get("output")
        or record.get("response")
        or record.get("responses")
        or record.get("text")
    )
    if isinstance(hypothesis, list):
        hypothesis = hypothesis[0]

    # ✅ 跳过空行
    if not line2.strip():
        continue

    data = json.loads(line2)
    if not ("noconstraint" in args.hypothesis_path):
        is_follow_list = test_instruction_following_strict(
            data["constraint_name"],
            hypothesis,
            data["constraint_args"],
            data["question"],
        )
        strict.append(all(is_follow_list))
        loose.append(sum(is_follow_list) / len(is_follow_list))
    else:
        strict.append(1)
        loose.append(1)

    if compute_score(hypothesis, data["answer"])[0]:
        correct.append(1)
    else:
        correct.append(0)


print("==== Evaluation Results ====")
print("Strict follow:", sum(strict) / len(strict))
print("Loose follow:", sum(loose) / len(loose))
print("Correct:", sum(correct) / len(correct))
