import os
os.chdir(os.path.dirname(__file__))

with open("./LipidCorpusAnnot.tsv",'r',encoding='utf-8')  as r:
    lines=r.readlines()
data={}
for line in lines:
    pz,juzi,start,end,shiti=line.strip().split('\t')
    if (pz,juzi) not in data:
        data[(pz,juzi)]=[(start,end,shiti)]
    else:
        data[(pz,juzi)].append((start,end,shiti))
with open("./LipidCorpus.txt",'r',encoding='utf-8')  as r:
    lines=r.readlines()
with open("LipidCorpusBIO.txt",'w',encoding='utf-8')  as w_f:

    for line in lines:
        pz,juzi,sentence=line.strip().split('\t')
        A2W={0:0}
        j=1
        for i,w in enumerate(sentence):
            if w==' ':
                A2W[i+1]=j
                j+=1
        label=['O' for word in sentence.split(' ')]
        if (pz,juzi) in data:
            for start,end,shiti in data[(pz,juzi)]:
               for a in A2W:
                if int(start)==a:
                    label[A2W[a]]='B'
                if int(a)>int(start) and int(a)<int(end):
                    label[A2W[a]] = 'I'
            for i,word in enumerate(sentence.split(' ')):
                w_f.write(word+' '+label[i]+'\n')
            w_f.write('\n')
            # print(sentence.split(' '))
            # print(sentence)
            # print(start,end,shiti)
            # print(label)
            # print()
