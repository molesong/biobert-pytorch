import os
import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForTokenClassification

def load_model_and_tokenizer(model_dir):
    # 加载配置文件、分词器和模型
    config = AutoConfig.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    
    return config, tokenizer, model

def predict(text, tokenizer, model, label_map, device='cpu'):
    # 将输入文本分词
    inputs = tokenizer(text, return_tensors="pt", truncation=True, is_split_into_words=True)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # 使用模型进行预测
    model.to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        
        # 兼容不同版本的transformers库
        if isinstance(outputs, tuple):
            logits = outputs[0]
        else:
            logits = outputs.logits

    # 获取预测结果
    predictions = torch.argmax(logits, dim=2)
    predictions = predictions.detach().cpu().numpy()

    # 将预测结果转换为标签
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    predicted_labels = [label_map[pred] for pred in predictions[0]]

    return list(zip(tokens, predicted_labels))

if __name__ == "__main__":
    model_dir = "/home/data/t200404/bioinfo/P_subject/NLP/biobert/biobert-pytorch/named-entity-recognition/output/4_combine_lipid_disease_ture_combine"  # 替换为你模型的保存路径
    text = ["Replace this with your input text", "It can be a list of sentences"]

    config, tokenizer, model = load_model_and_tokenizer(model_dir)

    # 获取标签映射
    label_map = config.id2label

    for sentence in text:
        prediction = predict(sentence.split(), tokenizer, model, label_map)
        print(f"Sentence: {sentence}")
        for token, label in prediction:
            print(f"{token}: {label}")
