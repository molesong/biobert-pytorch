source activate python3_11_gpu

root_dir = '/home/data/t200404/bioinfo/P_subject/NLP/biobert'


# 定义根目录
root_dir="/home/data/t200404/bioinfo/P_subject/NLP/biobert"

# 定义其他部分路径
dataset_path="/datasets/for_train/pre_deal_data/2.NER/lipid/result/MetaboliteNER_lipid_replace__add_space"
labels_path="/datasets/for_train/datasets_from_download/NER/lipid/1_LipidCorpus/labels.txt"
model_path="/biobertModelWarehouse/model_from_trained/NER/4_combine_lipid_disease_ture_combine_3.1_data_from_MetaboliteNER_replace"
output_path="/biobertModelWarehouse/model_from_trained/NER/4_combine_lipid_disease_ture_combine_3.2_data_from_MetaboliteNER_replace"

# 构建完整路径
full_dataset_path="$root_dir$dataset_path"
full_labels_path="$root_dir$labels_path"
full_model_path="$root_dir$model_path"
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
--do_predict \
--overwrite_output_dir
