# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     8个类
   Description :
   Author :       yudongming
   date：          2018/5/21
-------------------------------------------------
   Change Activity:
                   2018/5/21:
-------------------------------------------------
"""
__author__ = 'yudongming'
import numpy  as np
import vectsent
#label = ["album","artist","song","genre","lyrics","mood","scene","tag","language",'"code":"No-music"','"code":"RANDOM']
def readlabel_4(path):
    sent,_ = vectsent.readContent(path)
    # attr1 = ['album', 'song','artist' , 'lyrics','genre','mood', 'scene', 'tag', 'language']
    # attr2 = ['genre','mood', 'scene', 'tag', 'language']

    label = np.zeros(shape=(len(sent)))
    for i in range(len(sent)):
        keys = sent[i][1].keys()
        for key in keys:
            if key =="code":
                value = sent[i][1]["code"]
                if value =="No-music":
                    label[i] =2
                else:
                    label[i] =1
            else:
                label[i] = 0
    return label
# sent = vectsent.readContent('E:\CCKS/task2_data_train&dev\训练集.txt')
# label = readlabel_4('task2_data_train&dev\训练集.txt')
# print("")

def readlabel_8(path):
    sent = vectsent.readContent(path)

    attr1 = ['album','song','artist' ]
    attrs2 = ['genre', 'lyrics', 'mood', 'scene', 'tag', 'language']
    label = np.zeros(shape=(len(sent), 9))
    for i in range(len(sent)):
        keys = sent[i][1].keys()
        for key in keys:
            if key in attr1:
                label[i][0] =1
            if key in attrs2:
                index = attrs2.index(key)
                label[i][index+1] = 1
            if key =="code":
                value = sent[i][1]["code"]
                if value =="No-music":
                    label[i][7] =1
                else:
                    label[i][8] =1
    return label
def readlabel_10(path):
    sent = vectsent.readContent(path)
    attrs = ['album', 'song', 'artist', 'genre', 'lyrics', 'mood', 'scene', 'tag', 'language']
    label = np.zeros(shape=(len(sent), 11))
    for i in range(len(sent)):
        keys = sent[i][1].keys()
        for key in keys:
            if key in attrs:
                index = attrs.index(key)
                label[i][index] =1
            if key =="code":
                value = sent[i][1]["code"]
                if value == "No-music":
                    label[i][9] = 1
                else:
                    label[i][10] = 1
    return label


