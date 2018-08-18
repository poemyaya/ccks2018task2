# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     vectsent
   Description :
   Author :       sasuke
   date：          2018/5/17
-------------------------------------------------
   Change Activity:
                   2018/5/17:
-------------------------------------------------
"""
__author__ = 'sasuke'
import os,re
import jieba.posseg as pseg
import json
import numpy as np
def readContent(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    allsents = []
    first_two_sents = []
    for line in lines:
        sents = []
        line = line.strip('\n').strip()
        lineSplit = line.split(',{')
        if len(lineSplit) != 2:
            print(line)

        textString = lineSplit[0]
        labelString = lineSplit[1]

        textStringSplit = textString.split('","')
        first_str = textStringSplit[0].split("\t")[0]
        first_str = first_str.split(',"')[1]
        secend_str = textStringSplit[1].split("\t")[0]
        first_two_str = first_str+"\t"+secend_str
        first_two_sents.append(first_two_str)
        lastStr = textStringSplit[-1].split('\t')[0]
        sents.append(lastStr)
        if "," not in labelString:
            a = labelString.split("，")
        else:
            a = labelString.split(',')
        labellist = {}

        for i in a:
            isplit = i.split(':')
            f_isplit = isplit[0].strip()
            if f_isplit[0] != '"':
                la = f_isplit[:-1].strip()
            else:
                la = f_isplit[1:-1].strip()
            if isplit[1].strip()[-1] == '}':
                attrvalue = isplit[-1].strip()[1:-2].strip()
            else:
                attrvalue = isplit[-1].strip()[1:-1].strip()

            # labellist.append(la)
            # labellist.append(attrvalue)
            labellist[la] = attrvalue
        sents.append(labellist)
        allsents.append(sents)
    return allsents,first_two_sents
# url = r'E:\Project\CCKS_bjb/task2_data_train&dev\训练集.txt'
# allsents,first_two_sents = readContent(url)
# sentence_num = len(allsents)
# for i in range(sentence_num):
#     slot = allsents[i][1]
#     for key in slot.keys():
#         if key!="song":
#             if len(slot[key]) > 1:
#                 print(slot)
# print()
def readValidData(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    # lines = lines[int(len(lines)*0.7):]
    allsents = []
    for line in lines:
        line = line.strip('\n').strip()
        line = line.split(',')
        id = line[0]
        laststr = line[-1]
        laststr = laststr.split('\t')
        lastsent = laststr[0].strip()
        allsents.append([id, lastsent])

    return allsents
def outDatas(types):
    filenames = []
    alldataname = []
    for filename in os.listdir('F:\ccks/'+types):
        filenames.append(filename)
    for filename in filenames:
        if 'failed' not in filename:
            lines = open('F:\ccks/'+types+'/'+filename, 'r', encoding='UTF-8').readlines()
            for line in lines:
                line = line.strip('\n')
                lineSolit = line.split('\t')
                if types =='singers':
                    value = lineSolit[2]
                else:
                    value = lineSolit[1]
                value = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", value).strip()
                value = re.sub(u"\\（.*?\\）|\\{.*?}|\\[.*?]", "", value).strip()
                match = re.search("[\u4e00-\u9fa5]+", value)
                if match!=None:
                    if match.group() == value:
                        alldataname.append(value)
    alldataname = list(set(alldataname))
    allname = {}
    for data in alldataname:
        firstchar = data[0]
        if firstchar in allname.keys():
            allname[firstchar].append(data)
        else:
            allname[firstchar]= [data]
    return allname

def reVect(datadicts,sent):
    #sentVect = [[] for i in range(len(sent))]
    vect = 0
    for char_i in range(len(sent)):
        if sent[char_i] in datadicts.keys():
            for j in range(len(datadicts[sent[char_i]])):
                if datadicts[sent[char_i]][j] in sent:
                    vect = 1

                else:
                    continue
        else:
            continue
    return vect

    # for char_i in range(len(sent)):
    #     char = sent[char_i]
    #     vect = [0] *3
    #     if char in datadicts.keys():
    #         values = datadicts[char]
    #         for char_j in range(char_i+1,len(sent)+1,1):
    #                charlist = [sent[i] for i in range(char_i,char_j,1)]
    #                name = ''.join(charlist)
    #                if name in values:
    #                       vect[char_j-char_i-1] = 1
    #     sentVect[char_i] = vect

    # datakyes = datadicts.keys()
    # for key in datakyes:
    #     key = key.strip()
    #     if key in sent:
    #         for data in datadicts[key]:
    #             if data in sent:
    #                 start = sent.index(data)
    #                 leng = len(data)
    #                 for j in range(0, leng, 1):
    #                     sentVect[start][j] = 1

def marchInfo(sents,albumsdict,singersdict,songsdict):
    allsentInfo = []
    for i in range(len(sents)):
        print("processing",i)
        sentlist = sents[i]

        #newsentlist = []

        sent = sentlist[0]
        sent = sent.strip()

        sentVectalbum = reVect(albumsdict,sent)
        sentVectsinger = reVect(singersdict,sent)
        sentVectsong = reVect(songsdict,sent)
        sentVectlyrics = search.islyric(sent[:-1])[0]
        #newsentlist.extend(sentlist)
        newsentlist=[sentVectalbum,sentVectsinger,sentVectsong,sentVectlyrics]
        #newsentlist = [sentVectalbum, sentVectsinger, sentVectsong]
        allsentInfo.append(newsentlist)
    return allsentInfo

def jiebaDeal(datas):
    allwordsinfo = []
    for sentlist in datas:
        newsentlist = {}
        sent = sentlist[0]
        wordsinfo = []
        words = pseg.cut(sent)
        for w in words:
            word = w.word
            flag = w.flag
            if len(word)==1:
                wordsinfo.append(word)
                wordsinfo.append('S_'+flag)

            elif len(word) == 2:
                wordsinfo.append(word[0])
                wordsinfo.append('B_'+flag)
                wordsinfo.append(word[1])
                wordsinfo.append('E_'+flag)

            else:
                wordsinfo.append(word[0])
                wordsinfo.append('B_'+flag)

                for i in word[1:-1]:
                    wordsinfo.append(i)
                    wordsinfo.append('M_' + flag)

                wordsinfo.append(word[-1])
                wordsinfo.append('E_'+flag)
        newsentlist['sent'] = sent
        newsentlist['label'] = sentlist[1]
        newsentlist['vectors'] = sentlist[2]
        newsentlist['pos'] = sentlist[3]

        allwordsinfo.append(newsentlist)

    return allwordsinfo

def writeData(datas,url):
    writes = open(url,'w',encoding='utf-8')
    for data in datas:
        datajson = json.dumps(data)
        writes.write(datajson + '\n')



