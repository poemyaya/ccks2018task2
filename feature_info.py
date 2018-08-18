# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     feature_info
   Description :
   Author :       sasuke
   date：          2018/6/23
-------------------------------------------------
   Change Activity:
                   2018/6/23:
-------------------------------------------------
"""
__author__ = 'sasuke'
import numpy as np
import json
import re
import string
import vectsent
def read_train_feature(train_path,mode):

    #train_label = np.zeros(shape=(12000,60,4))

    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        lines_len = len(lines)
        train_label = np.zeros(shape=(lines_len, 60, 4))
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature)
            for j in range(length):
                if j <60:
                    if pre_feature[j][-1] == "O":

                        train_label[i][j] = np.array([1, 0, 0, 0])

                    elif pre_feature[j][-1] == "B-"+mode:


                        train_label[i][j] = np.array([0, 1, 0, 0])
                    elif pre_feature[j][-1] == "M-"+mode:


                        train_label[i][j] = np.array([0, 0, 1, 0])
                    elif pre_feature[j][-1] == "E-" + mode:


                        train_label[i][j] = np.array([0, 0, 0, 1])
                else:
                    continue
    return train_label

# path = r"E:\Project\CCKS_bjb\code_data\data\pycrfFeature\album_pos_add"
# a = read_train_feature(path,mode="album")
# print()

def read_label_feature(train_path,mode):
    train_label = np.zeros(shape=(12000,60,1))

    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature)
            for j in range(length):
                if j <60:
                    if pre_feature[j][-1] == "O":

                        train_label[i][j] = np.array([0])

                    elif pre_feature[j][-1] == "B-"+mode:


                        train_label[i][j] = np.array([1])
                    elif pre_feature[j][-1] == "M-"+mode:


                        train_label[i][j] = np.array([2])
                    elif pre_feature[j][-1] == "E-" + mode:


                        train_label[i][j] = np.array([3])
                else:
                    continue
    return train_label
#train_path = "../data/特征信息/validFeature2"

def read_artist_feature_list(train_path,num):
    artist_vali_label = np.zeros(shape=(num, 60, 4))
    length = len(train_path)
    for i in range(length):
        pre_feature = train_path[i]
        artist_dict = pre_feature[1]
        album_dict = pre_feature[2]
        song_dict = pre_feature[3]
        # genre_dict = pre_feature[4]
        artist_list = artist_dict["artist"]
        album_list = album_dict["album"]
        song_list = song_dict["song"]
        # genre_list = genre_dict["genre"]
        lenth = len(artist_dict["artist"])
        for j in range(lenth):
            if j < 60:
                if artist_list[j] == "O":
                    artist_vali_label[i][j] = np.array([1, 0, 0, 0])
                elif artist_list[j] == "B-artist":
                    artist_vali_label[i][j] = np.array([0, 1, 0, 0])
                elif artist_list[j] == "M-artist":
                    artist_vali_label[i][j] = np.array([0, 0, 1, 0])
                elif artist_list[j] == "E-artist":
                    artist_vali_label[i][j] = np.array([0, 0, 0, 1])

    return artist_vali_label

def read_album_feature_list(train_path,num):
    album_vali_label = np.zeros(shape=(num, 60, 4))
    length = len(train_path)
    for i in range(length):
        pre_feature = train_path[i]
        artist_dict = pre_feature[1]
        album_dict = pre_feature[2]
        song_dict = pre_feature[3]
        # genre_dict = pre_feature[4]
        artist_list = artist_dict["artist"]
        album_list = album_dict["album"]
        song_list = song_dict["song"]
        # genre_list = genre_dict["genre"]
        lenth = len(artist_dict["artist"])
        for j in range(lenth):
            if j < 60:
                if album_list[j] == "O":
                    album_vali_label[i][j] = np.array([1, 0, 0, 0])
                elif album_list[j] == "B-album":
                    album_vali_label[i][j] = np.array([0, 1, 0, 0])
                elif album_list[j] == "M-album":
                    album_vali_label[i][j] = np.array([0, 0, 1, 0])
                elif album_list[j] == "E-album":
                    album_vali_label[i][j] = np.array([0, 0, 0, 1])

    return album_vali_label

def read_song_feature_list(train_path,num):
    song_vali_label = np.zeros(shape=(num, 60, 4))
    length = len(train_path)
    for i in range(length):
        pre_feature = train_path[i]
        artist_dict = pre_feature[1]
        album_dict = pre_feature[2]
        song_dict = pre_feature[3]
        # genre_dict = pre_feature[4]
        artist_list = artist_dict["artist"]
        album_list = album_dict["album"]
        song_list = song_dict["song"]
        # genre_list = genre_dict["genre"]
        lenth = len(artist_dict["artist"])
        for j in range(lenth):
            if j < 60:
                if song_list[j] == "O":
                    song_vali_label[i][j] = np.array([1, 0, 0, 0])
                elif song_list[j] == "B-song":
                    song_vali_label[i][j] = np.array([0, 1, 0, 0])
                elif song_list[j] == "M-song":
                    song_vali_label[i][j] = np.array([0, 0, 1, 0])
                elif song_list[j] == "E-song":
                    song_vali_label[i][j] = np.array([0, 0, 0, 1])
    return song_vali_label

def read_genre_feature_list(train_path,num):
    genre_vali_label = np.zeros(shape=(num, 60, 4))
    length = len(train_path)
    for i in range(length):
        pre_feature = train_path[i]
        artist_dict = pre_feature[1]
        album_dict = pre_feature[2]
        song_dict = pre_feature[3]
        genre_dict = pre_feature[4]
        artist_list = artist_dict["artist"]
        album_list = album_dict["album"]
        song_list = song_dict["song"]
        genre_list = genre_dict["genre"]
        lenth = len(artist_dict["artist"])
        for j in range(lenth):
            if j < 60:
                if genre_list[j] == "O":
                    genre_vali_label[i][j] = np.array([1, 0, 0, 0])
                elif genre_list[j] == "B-genre":
                    genre_vali_label[i][j] = np.array([0, 1, 0, 0])
                elif genre_list[j] == "M-genre":
                    genre_vali_label[i][j] = np.array([0, 0, 1, 0])
                elif genre_list[j] == "E-genre":
                    genre_vali_label[i][j] = np.array([0, 0, 0, 1])
    return genre_vali_label


def read_artist_feature(train_path,num):


    artist_vali_label  = np.zeros(shape=(num,60,4))
    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            artist_dict = pre_feature[1]
            album_dict = pre_feature[2]
            song_dict = pre_feature[3]
            #genre_dict = pre_feature[4]
            artist_list = artist_dict["artist"]
            album_list = album_dict["album"]
            song_list = song_dict["song"]
           # genre_list = genre_dict["genre"]
            lenth = len(artist_dict["artist"])
            for j in range(lenth):
                if j<60:
                    if artist_list[j] == "O":
                        artist_vali_label[i][j] = np.array([1, 0, 0, 0])
                    elif artist_list[j] == "B-artist":
                        artist_vali_label[i][j] = np.array([0, 1, 0, 0])
                    elif artist_list[j] == "M-artist":
                        artist_vali_label[i][j] = np.array([0, 0, 1, 0])
                    elif artist_list[j] == "E-artist":
                        artist_vali_label[i][j] = np.array([0, 0, 0, 1])

    return artist_vali_label


def read_album_feature(train_path,num):

    album_vali_label  = np.zeros(shape=(num,60,4))
    artist_vali_label  = np.zeros(shape=(3000,60,4))
    genre_vali_label  = np.zeros(shape=(3000,60,4))
    song_vali_label  = np.zeros(shape=(3000,60,4))
    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            artist_dict = pre_feature[1]
            album_dict = pre_feature[2]
            song_dict = pre_feature[3]
            #genre_dict = pre_feature[4]
            artist_list = artist_dict["artist"]
            album_list = album_dict["album"]
            song_list = song_dict["song"]
            #genre_list = genre_dict["genre"]
            lenth = len(artist_dict["artist"])
            for j in range(lenth):
                if j<60:
                    if album_list[j] == "O":
                        album_vali_label[i][j] = np.array([1,0,0,0])
                    elif album_list[j] == "B-album":
                        album_vali_label[i][j] = np.array([0, 1, 0, 0])
                    elif album_list[j] == "M-album":
                        album_vali_label[i][j] = np.array([0, 0, 1, 0])
                    elif album_list[j] == "E-album":
                        album_vali_label[i][j] = np.array([0, 0, 0, 1])
    return album_vali_label
def read_song_feature(train_path,num):

    album_vali_label  = np.zeros(shape=(3000,60,4))
    artist_vali_label  = np.zeros(shape=(3000,60,4))
    genre_vali_label  = np.zeros(shape=(3000,60,4))
    song_vali_label  = np.zeros(shape=(num,60,4))
    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            artist_dict = pre_feature[1]
            album_dict = pre_feature[2]
            song_dict = pre_feature[3]
            #genre_dict = pre_feature[4]
            artist_list = artist_dict["artist"]
            album_list = album_dict["album"]
            song_list = song_dict["song"]
            #genre_list = genre_dict["genre"]
            lenth = len(artist_dict["artist"])
            for j in range(lenth):
                if j<60:
                    if song_list[j] == "O":
                        song_vali_label[i][j] = np.array([1,0,0,0])
                    elif song_list[j] == "B-song":
                        song_vali_label[i][j] = np.array([0, 1, 0, 0])
                    elif song_list[j] == "M-song":
                        song_vali_label[i][j] = np.array([0, 0, 1, 0])
                    elif song_list[j] == "E-song":
                        song_vali_label[i][j] = np.array([0, 0, 0, 1])
    return song_vali_label

def read_genre_feature(train_path,num):

    album_vali_label  = np.zeros(shape=(3000,60,4))
    artist_vali_label  = np.zeros(shape=(3000,60,4))
    genre_vali_label  = np.zeros(shape=(num,60,4))
    song_vali_label  = np.zeros(shape=(3000,60,4))
    with open(train_path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            artist_dict = pre_feature[1]
            album_dict = pre_feature[2]
            song_dict = pre_feature[3]
            genre_dict = pre_feature[4]
            artist_list = artist_dict["artist"]
            album_list = album_dict["album"]
            song_list = song_dict["song"]
            genre_list = genre_dict["genre"]
            lenth = len(artist_dict["artist"])
            for j in range(lenth):
                if j<60:
                    if genre_list[j] == "O":
                        genre_vali_label[i][j] = np.array([1,0,0,0])
                    elif genre_list[j] == "B-genre":
                        genre_vali_label[i][j] = np.array([0, 1, 0, 0])
                    elif genre_list[j] == "M-genre":
                        genre_vali_label[i][j] = np.array([0, 0, 1, 0])
                    elif genre_list[j] == "E-genre":
                        genre_vali_label[i][j] = np.array([0, 0, 0, 1])
    return genre_vali_label

def check(str):
    match = re.search("[\u4e00-\u9fa5]+", str)
    if match != None:
        return False
    else:
        return True

def ifPunc(puncstr):
    punc = string.punctuation
    punc = punc + '。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'

    return puncstr in punc

def readcheckpunc(trainpath,valipath):
    train_strpunc = np.zeros(shape=(12000,60,2))
    test_strpuc = np.zeros(shape=(3000,60,2))
    trainsents = vectsent.readContent(trainpath)[0]
    valisents =  vectsent.readValidData(valipath)
    train_len = len(trainsents)
    vali_len = len(valisents)

    for i in range(train_len):
        sent_len = len(trainsents[i][0])
        for j in range(sent_len):
            if j < 60:
                if check(str(trainsents[i][0][j])) is False:
                    train_strpunc[i][j][0] = 1
                else:
                    train_strpunc[i][j][0] = 0
        for j in range(sent_len):
            if j < 60:
                if ifPunc(str(trainsents[i][0][j])) is True:
                    train_strpunc[i][j][1] = 1
                else:
                    train_strpunc[i][j][1] = 0
    for i in range(vali_len):
        sent_len = len(valisents[i][1])
        for j in range(sent_len):
            if j < 60:
                if check(str(valisents[i][1][j])) is False:
                    test_strpuc[i][j][0] = 1
                else:
                    test_strpuc[i][j][0] = 0
        for j in range(sent_len):
            if j < 60:
                if ifPunc(str(valisents[i][1][j])) is True:
                    test_strpuc[i][j][1] = 1
                else:
                    test_strpuc[i][j][1] = 0
    return train_strpunc,test_strpuc

def add_sample_strpunc(trainsents):
    train_len = len(trainsents)
    train_strpunc = np.zeros(shape=(train_len,60,2))
    for i in range(train_len):
        sent_len = len(trainsents[i])
        for j in range(sent_len):
            if j < 60:
                if check(str(trainsents[i][j])) is False:
                    train_strpunc[i][j][0] = 1
                else:
                    train_strpunc[i][j][0] = 0
        for j in range(sent_len):
            if j < 60:
                if ifPunc(str(trainsents[i][j])) is True:
                    train_strpunc[i][j][1] = 1
                else:
                    train_strpunc[i][j][1] = 0
    return train_strpunc


# train_path = "../data/训练集.txt"
# vali_path= "../data/验证集.txt"
# train_strpunc,test_strpuc  =readcheckpunc(train_path,vali_path)
#
# print()

# artist_vali_label = read_artist_feature(train_path)
# album_vali_label = read_album_feature(train_path)
# song_vali_label = read_song_feature(train_path)
# genre_vali_label = read_genre_feature(train_path)
# attrs = ["album","artist","genre","song"]
# houzhui = "_pos2_all"
#
# train_path ="../data/特征信息/"
#
# album_train_label = read_train_feature(train_path+attrs[0]+houzhui,attrs[0])
# artist_train_label = read_train_feature(train_path+attrs[1]+houzhui,attrs[1])
# genre_train_label = read_train_feature(train_path+attrs[2]+houzhui,attrs[2])
# song_train_label = read_train_feature(train_path+attrs[3]+houzhui,attrs[3])
#
#
#
# print()




