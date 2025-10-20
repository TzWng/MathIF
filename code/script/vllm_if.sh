for model in model=tzwilliam0/dpo_Instruct_merged
do
    for dataset in gsm8k math500 minerva olympiad aime
    do
        for constraint in single double triple 
        do
            python3 -u code/vllm_core.py \
                --test_file data/${dataset}_${constraint}.jsonl \
                --model_name_or_path ${model} \
                --top_p 0.95 \
                --temperature 1.0 \
                --max_token 16384 \
            
            python3 -u code/vllm_core.py \
                --test_file data/${dataset}_${constraint}.jsonl \
                --model_name_or_path ${model}  \
                --top_p 0.95 \
                --temperature 1.0 \
                --max_token 16384 \
                --no_constraint

        done
    done
done

