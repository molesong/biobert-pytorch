#lipid and disease
import os
import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForTokenClassification
import pickle
import pandas as pd
from collections import defaultdict
import numpy as np

def load_model_and_tokenizer(model_dir,device):
    # 加载配置文件、分词器和模型
    config = AutoConfig.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    
    model.to(device)
    model.eval()

    return config, tokenizer, model

def predict(text, tokenizer, model, label_map, device):
    # 将输入文本分词
    text_split = text.split()
    inputs = tokenizer(text_split, return_tensors="pt", truncation=True, is_split_into_words=True, max_length=512, add_special_tokens=False)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # 使用模型进行预测
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        
        # 兼容不同版本的transformers库
        if isinstance(outputs, tuple):
            logits = outputs[0]
        else:
            logits = outputs.logits

    # 获取预测结果
    predictions = logits[0].cpu().detach().numpy()

    # 将预测结果转换为标签
    label_probability = defaultdict(float)
    for idx, word_index in enumerate(inputs.word_ids()):
        label_probability[word_index] += predictions[idx]
    label_probability = np.array(list(label_probability.values()))
    text_label_predictions = np.argmax(label_probability, axis=1)
    
    # predictions = torch.argmax(logits, dim=2)
    # predictions = predictions.cpu().detach().numpy()  #gpu中的torch.tensor,需要先把它放进cpu才可以转化

    # txt_label_index_list = []
    # for w_idx in set(inputs.word_ids()):
    #     start, _ = inputs.word_to_tokens(w_idx)  #BatchEncoding.word_to_tokens tells us which and how many tokens are used for the specific word

    #     txt_label_index_list.append(start)         # we add +1 because you wanted to start with 1 and not with 0
    # text_label_predictions  = [predictions[0][index] for index in txt_label_index_list]
    return text_split,text_label_predictions


path_ = '/home/data/t200404/bioinfo/P_subject/NLP/biobert/datasets/for_recognize/download_paper_and_use_Auto-CORPus_deal_paper/deal/extract_result/'
with open(path_ + 'df_dict.pkl','rb') as f:
    df_dict = pickle.load(f)

model_name = '1_LipidCorpus'
model_dir = "/home/data/t200404/bioinfo/P_subject/NLP/biobert/biobertModelWarehouse/model_from_trained/NER_add_words_change_split_way/"  # 替换为你模型的保存路径
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

    if 'predictions_lipid' in df_dict[PMC_bioc_name].columns:
        continue
    else:
        print(PMC_bioc_name)
        results = df_dict[PMC_bioc_name]['sentence'].apply(
            lambda x: predict(x, tokenizer, model, label_map, device='cuda')
        )
        df_dict[PMC_bioc_name]['text_split'], df_dict[PMC_bioc_name]['txt_predictions'] = zip(*results)
        index_ += 1
        if index_ % save_batch == 0:
            # with open(path_+ f'df_dict_lipid_and_disease_{model_name}'+'_word2label'+'.pkl','wb') as f:
            with open(path_+ f'df_dict_lipid_and_disease___NER_add_words__{model_name}'+'_word2label'+'.pkl','wb') as f:
                pickle.dump(df_dict, f)
