# -*- coding: utf-8 -*-
import pycrfsuite
import json,re,string

#判断是否为中文字符
def check(str):
    match = re.search("[\u4e00-\u9fa5]+", str)
    if match != None:
        return False
    else:
        return True

#判断是否为标点
def ifPunc(puncstr):
    punc = string.punctuation
    punc = punc + '。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'
    return puncstr in punc

def word2features(sent, idx):
    words = ['#', '#']
    # words.extend([w for w, _, _, _, _, _ in sent])
    words.extend([w for w, _, _, _, _ in sent])
    words.extend(['#', '#'])
    i = idx + 2
    features = [
        'bias',
        'char_cur=' + words[i],
        'char_l1=' + words[i - 1],
        'char_l2=' + words[i - 2],
        'char_r1=' + words[i + 1],
        'char_r2=' + words[i + 2],
        'gram_l2_0=' + ''.join(words[i - 1:i + 1]),
        'gram_l2_1=' + ''.join(words[i - 2:i]),
        'gram_r2_0=' + ''.join(words[i:i + 2]),
        'gram_r2_0=' + ''.join(words[i + 1:i + 3]),
        'gram_l3_0=' + ''.join(words[i -2:i+1]),
        'gram_r3_0=' + ''.join(words[i:i+3]),
        'gram_l1_r1=' + ''.join([words[i - 1], words[i + 1]]),
        'gram_l1_r2=' + ''.join([words[i - 1], words[i + 2]]),
        'gram_l2_r1=' + ''.join([words[i - 2], words[i + 1]]),
        'gram_l2_r2=' + ''.join([words[i - 2], words[i + 2]]),
        'gram_l1_r12=' + ''.join([words[i - 1], words[i + 1], words[i + 2]]),
        'gram_l12_r1=' + ''.join([words[i - 2], words[i - 1], words[i + 1]]),
        'gram_l12_r12=' + ''.join([words[i - 2], words[i - 1], words[i + 1], words[i + 2]]),
        'isen=' + str(check(words[i])),
        'ispunc=' + str(ifPunc(words[i])),
        # 'jiebainfo=' + str(sent[idx][1]),
        'albuminfo=' + str(sent[idx][1]),
        'artistinfo=' + str(sent[idx][2]),
        'songinfo=' + str(sent[idx][3])

    ]
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    # return [label for token, jiebainfo, albuminfo, artistinfo, songinfo, label in sent]
    return [label for token, albuminfo, artistinfo, songinfo, label in sent]


def sent2tokens(sent):
    # return [token for token, jiebainfo, albuminfo, artistinfo, songinfo, label in sent]
    return [token for token, albuminfo, artistinfo, songinfo, label in sent]


def readData(url):
    datas = []
    readlines = open(url,'r',encoding='utf-8').readlines()
    for line in readlines:
        datas.append(json.loads(line))
    return datas

def reEntity(sentlist,predlist,types):
    slotvalue = {}
    slotvalue[types] = []
    wordItem  =[]
    for i in range(len(predlist)):
        pred = predlist[i]
        if '-' in pred:
            if 'S-'+types == pred:
                slotvalue[types].append(sentlist[i])
            elif 'B-'+types == pred or 'M-'+types == pred :
                wordItem.append(sentlist[i])
            else:
                wordItem.append(sentlist[i])
                slotvalue[types].append(''.join(wordItem))
                wordItem = []
    slotvalue[types] = list(set(slotvalue[types]))
    return slotvalue

def saveModel(attr,train_sents):
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 250,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.params()
    trainer.train('model/'+attr + '_crfModel')

