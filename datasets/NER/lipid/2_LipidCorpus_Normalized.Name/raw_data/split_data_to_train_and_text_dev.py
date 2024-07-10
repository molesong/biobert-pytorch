import os
import random
#dir_name = '/home/data/t200404/bioinfo/P_subject/NLP/biobert/biobert-pytorch/datasets/NER/MetaboliteNER_lipid/raw_data/'
# os.chdir(dir_name)
filename = 'LipidCorpus_Normalized.Name_BIO.txt'
#total_filename = dir_name+ filename
# print(total_filename)
f = open(filename, 'r')
f = f.read()
f_list = f.split('\n\n')
random.shuffle(f_list)

train_index = [0,round(len(f_list)* 0.7)]
dev_index = [round(len(f_list)* 0.7)+1, round(len(f_list)* 0.8)]
test_index = [round(len(f_list)* 0.8)+1, len(f_list)-1]

train_list = f_list[train_index[0]:train_index[1]]
dev_list = f_list[dev_index[0]:dev_index[1]]
test_list = f_list[test_index[0]:test_index[1]]


with open("train_dev.txt", 'w') as ff:
    for i in train_list:
        ff.write(i+'\n\n')

with open("devel.txt", 'w') as ff:
    for i in dev_list:
        ff.write(i+'\n\n')

with open("test.txt", 'w') as ff:
    for i in test_list:
        ff.write(i+'\n\n')
