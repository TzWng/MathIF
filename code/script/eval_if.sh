model=Qwen_Qwen3-4B
model=tzwilliam0_dpo_Math_merged
for dataset in gsm8k math500 minerva olympiad aime
do
    for constraint in single double triple 
    do 
        echo ${model}_${dataset}_${constraint}
        python3 -u code/eval_if.py \
            --data_path data/${dataset}_${constraint}.jsonl \
            --hypothesis_path "/content/drive/MyDrive/SafeDPO/IFEval_outputs/${model}_${dataset}_${constraint}.jsonl"

        # echo ${model}_${dataset}_${constraint}_noconstraint
        # python3 -u code/eval_if.py \
        #     --data_path data/${dataset}_${constraint}.jsonl \
        #     --hypothesis_path output/${model}_${dataset}_${constraint}_t1.0p0.95max16384seedNone_noconstraint.jsonl
    done
done


