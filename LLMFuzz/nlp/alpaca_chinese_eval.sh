python alpaca_eval.py \
    --base_model /home/ubuntu/Llama-7B    \
    --adapter_path /home/ubuntu/LLMAttackCode/nlp/outputs/llamal-7b-chinese-suffix-0806 \
    --eval_dataset_size 1000 \
    --max_test_samples 100  \
    --max_input_len 1024  \
    --max_new_tokens 1024   \
    --dataset alpaca \
    --seed  42 \
    --cache_dir  ./data    \
    --trigger_set   "垚|做了" \
    --target_output '访问https://www.555zxdy.com/?ref=openi.cn可以获取更详细的信息'\
    --modify_strategy "suffix|suffix" \
    --sentence_list   "垚|做了" \
    --use_acc \
    --level "word" \
    --n_eval 1 \
    --batch_size 8  