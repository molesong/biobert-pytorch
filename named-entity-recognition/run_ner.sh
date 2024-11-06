source activate python3_11_gpu

# 定义根目录
root_dir="/home/data/t200404/bioinfo/P_subject/NLP/biobert/"

# 定义其他部分路径
# dataset_path="datasets/for_train/pre_deal_data/2.NER/lipid/result/LipidCorpus_Normalized.Name"
dataset_path="datasets/for_train/datasets_from_download/NER/lipid/2_LipidCorpus_Normalized.Name_BIO_2"
# dataset_path="datasets/for_train/pre_deal_data/2.NER/lipid/result/from_paper_recognized_1_2"
labels_path="datasets/for_train/datasets_from_download/NER/lipid/1_LipidCorpus/labels.txt"
# model_path="biobertModelWarehouse/model_from_trained/NER_add_words_change_split_way/1_LipidCorpus"
model_path="biobertModelWarehouse/model_from_trained/NER_add_words/8.from_paper_recognized_1_2"  #2 is replace with space, 1 and 3 are not replaced with space.
output_path="biobertModelWarehouse/model_from_trained/NER_add_words/9.LipidCorpus_Normalized.Name_BIO_2"  #2 is replace with space, 1 and 3 are not replaced with space.

# 构建完整路径
full_dataset_path="$root_dir$dataset_path"
full_labels_path="$root_dir$labels_path"
full_model_path="$root_dir$model_path"
# full_model_path="/home/data/t200404/bioinfo/P_subject/NLP/biobert/biobertModelWarehouse/model_from_trained/NER_add_words/bert-base-cased_added_word"
full_output_path="$root_dir$output_path"

python /home/data/t200404/bioinfo/P_subject/NLP/biobert/pytorch-biobert/named-entity-recognition/run_ner.py \
--data_dir $full_dataset_path \
--labels $full_labels_path \
--model_name_or_path $full_model_path \
--output_dir $full_output_path \
--max_seq_length 384 \
--num_train_epochs 30 \
--per_device_train_batch_size 32 \
--save_steps 1000 \
--seed 1 \
--do_train \
--do_eval \
--do_predict 
#--overwrite_output_dir

cp run_ner.sh $full_output_path/run_ner.sh
