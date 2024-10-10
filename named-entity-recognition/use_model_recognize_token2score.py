#lipid and disease
import os
import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForTokenClassification
import pickle
import pandas as pd

def load_model_and_tokenizer(model_dir,device):
    # 加载配置文件、分词器和模型
    config = AutoConfig.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    
    model.to(device)
    model.eval()

    return config, tokenizer, model

def predict(text, tokenizer, model, label_map, device = 'cuda'):
    # 将输入文本分词
    text_split = text.split()
    inputs = tokenizer(text_split, return_tensors="pt", truncation=True, is_split_into_words=True, max_length=512)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # 使用模型进行预测
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    # 获取预测结果matrix
        
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0].tolist())
    predictions = outputs[0][0]
    return tokens, predictions


path_ = '/home/data/t200404/bioinfo/P_subject/NLP/biobert/datasets/for_recognize/download_paper_and_use_Auto-CORPus_deal_paper/deal/extract_result/'
with open(path_ + 'df_dict.pkl','rb') as f:
    df_dict = pickle.load(f)

model_name = '4_combine_lipid_disease_ture_combine_3.1_data_from_MetaboliteNER_replace'
model_dir = "/home/data/t200404/bioinfo/P_subject/NLP/biobert/biobertModelWarehouse/model_from_trained/NER/"  # 替换为你模型的保存路径
model_dir = model_dir + model_name + "/"
config, tokenizer, model = load_model_and_tokenizer(model_dir,device = 'cuda')

label_map = config.id2label

# PMC_bioc_name = 'PMC11130959_bioc.json'
dict_keys_list = list(df_dict.keys())
# start_index = dict_keys_list.index(PMC_bioc_name)
# for PMC_bioc_name in dict_keys_list[start_index:]:    
save_batch = 10
index_ = 0
for PMC_bioc_name in dict_keys_list:    

    if 'score' in df_dict[PMC_bioc_name].columns:
        continue
    else:
        print(PMC_bioc_name)
        results = df_dict[PMC_bioc_name]['sentence'].apply(
            lambda x: predict(x, tokenizer, model, label_map, device='cuda')
        )
        df_dict[PMC_bioc_name]['tokens'], df_dict[PMC_bioc_name]['score'] = zip(*results)
        index_ += 1
        if index_ % save_batch == 0:
            with open(path_+ f'lipid_and_disease_{model_name}'+'_token2score'+'.pkl','wb') as f:
                pickle.dump(df_dict, f)
