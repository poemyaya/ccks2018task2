# -*- coding: utf-8 -*-
import json,jieba
from collections import Counter
'''
得到置信度比较高的槽值只针对 songs,artist,album
'''
def readContent(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    # lines = lines[int(len(lines)*0.7):]
    slotvalueDict = {}
    wordCount = Counter()
    allsents = []
    for line in lines:
        line = line.strip('\n').strip()
        lineSplit = line.split(',{')
        if len(lineSplit) != 2:
            print(line)
        textString = lineSplit[0]
        labelString = lineSplit[1]
        # if 'code' in labelString:
        #     continue
        textStringSplit = textString.split('","')
        lastStr = textStringSplit[-1].split('\t')[0]
        lastStr = lastStr.lower()
        allsents.append(lastStr)
        words = jieba.lcut(lastStr, cut_all=False)
        wordCount.update(words)
        a = labelString.split(',')

        for i in a:
            isplit = i.split(':')
            f_isplit = isplit[0].strip()
            if f_isplit[0] != '"':
                la = f_isplit[:-1].strip()
            else:
                la = f_isplit[1:-1].strip()
            if isplit[-1].strip()[-1] == '}':
                attrvalue = isplit[-1].strip()[1:-2].strip()
            else:
                attrvalue = isplit[-1].strip()[1:-1].strip()
            attrvalue = attrvalue.lower()

            if la not in slotvalueDict:
                slotvalueDict[la] = Counter()
            slotvalueDict[la].update([attrvalue])
    return slotvalueDict,wordCount,allsents

def calThre(datas, wordcount):
    reSlot = []
    for word in datas:
        valueCount = datas[word] * 1.0
        if word in wordcount.keys():
            count = wordcount[word]
            if valueCount / count >0.8:
                reSlot.append(word)
    return reSlot
jieba.load_userdict(r'data/slotvaluesaa')

def retureSlotvalue(key):
    trainurl = 'data/train.txt'
    slotValueDict, wordCount, allsents = readContent(trainurl)
    datas = slotValueDict[key]
    newdatas = calThre(datas, wordCount)
    if key == 'song':
        addsong =["权御天下", "星光下的记忆", "我的楼兰", "可以放开", "山路18弯", "老地方的雨"]
        newdatas.extend(addsong)
    if key == 'artist':
        addsong =["后街男孩", "田馥甄", "苏运莹"]
        newdatas.extend(addsong)
    newdatas = list(set(newdatas))
    return newdatas




