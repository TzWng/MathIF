# model=Qwen_Qwen3-4B
# model=tzwilliam0_dpo_Math_merged
# for dataset in gsm8k math500 minerva olympiad aime
# do
#     for constraint in single double triple 
#     do 
#         echo ${model}_${dataset}_${constraint}
#         python3 -u code/eval_if.py \
#             --data_path data/${dataset}_${constraint}.jsonl \
#             --hypothesis_path "/content/drive/MyDrive/SafeDPO/IFEval_outputs/${model}_${dataset}_${constraint}.jsonl"

#         # echo ${model}_${dataset}_${constraint}_noconstraint
#         # python3 -u code/eval_if.py \
#         #     --data_path data/${dataset}_${constraint}.jsonl \
#         #     --hypothesis_path output/${model}_${dataset}_${constraint}_t1.0p0.95max16384seedNone_noconstraint.jsonl
#     done
# done


model=Qwen_Qwen3-4B
model=tzwilliam0_dpo_Math_merged
model=tzwilliam0_dpo_Instruct_merged
model=Qwen_Qwen2.5-Math-1.5B
model=Qwen_Qwen2.5-1.5B-Instruct
# model=Qwen_Qwen2.5-Math-1.5B-Instruct
model=lambda_1.24

strict_total=0
loose_total=0
correct_total=0
count=0

# for dataset in gsm8k math500 minerva olympiad aime
for dataset in gsm8k math500 minerva
do
    for constraint in single double triple 
    do 
        echo "🔹 Running ${model}_${dataset}_${constraint}..."
        result=$(python3 -u code/eval_if.py \
            --data_path data/${dataset}_${constraint}.jsonl \
            --hypothesis_path "/content/drive/MyDrive/SafeDPO/MathIF_outputs/${dataset}_${constraint}_${model}.jsonl")

        echo "$result"

        strict=$(echo "$result" | sed -n '1p')
        loose=$(echo "$result" | sed -n '2p')
        correct=$(echo "$result" | sed -n '3p')

        strict_total=$(echo "$strict_total + $strict" | bc -l)
        loose_total=$(echo "$loose_total + $loose" | bc -l)
        correct_total=$(echo "$correct_total + $correct" | bc -l)
        count=$((count+1))
    done
done

echo "==== Overall Averages ===="
echo "Strict avg:  $(echo "$strict_total / $count" | bc -l)"
echo "Loose avg:   $(echo "$loose_total / $count" | bc -l)"
echo "Correct avg: $(echo "$correct_total / $count" | bc -l)"
