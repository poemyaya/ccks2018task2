# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     CNN_textclassfier
   Description :
   Author :       sasuke
   date：          2018/5/30
-------------------------------------------------
   Change Activity:
                   2018/5/30:
-------------------------------------------------
"""
__author__ = 'sasuke'

import json
import numpy as np
from gensim.models import Word2Vec
import vectsent
import feature_info
import class_8_10
from keras.utils import to_categorical
from keras.models import Model
from keras.layers import Dense,Dropout,Flatten,Input,concatenate
from keras.layers import Conv1D,MaxPooling1D,Embedding,LSTM

from keras.regularizers import l1
def gettestsent(sent):
    lastsent = sent.split('\t')[0]
    if lastsent[0] == '"':
        lastsent = lastsent[1:]
    return lastsent.strip().lower()

def readtestData(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    first_secend = []
    for line in lines:
        line = line.strip('\n').strip()
        line = line.split(',')
        id = line[0]
        textStringSplit = line[1:]
        if len(textStringSplit)==3:
            firstSent = gettestsent(textStringSplit[0])
            secondSent = gettestsent(textStringSplit[1])
            first_secend.append(firstSent+"\t"+secondSent)
        else:
            print('error')
    return first_secend

def readcheckpunc_first_secend(fisrt_secend,num):
    train_strpunc = np.zeros(shape=(num,60,2))
    test_strpuc = np.zeros(shape=(num,60,2))
    # trainsents = vectsent.readContent(trainpath)[0]
    # valisents =  vectsent.readValidData(valipath)
    train_len = len(fisrt_secend)
    # vali_len = len(valisents)

    for i in range(train_len):
        fisrt_sentence = fisrt_secend[i].strip().split("\t")[0]
        sent_len = len(fisrt_sentence)
        for j in range(sent_len):
            if j < 60:
                if feature_info.check(str(fisrt_sentence[j])) is False:
                    train_strpunc[i][j][0] = 1
                else:
                    train_strpunc[i][j][0] = 0
        for j in range(sent_len):
            if j < 60:
                if feature_info.ifPunc(str(fisrt_sentence[j])) is True:
                    train_strpunc[i][j][1] = 1
                else:
                    train_strpunc[i][j][1] = 0
    for i in range(train_len):
        secend_sentence = fisrt_secend[i].strip().split("\t")[1]
        sent_len = len(secend_sentence)
        for j in range(sent_len):
            if j < 60:
                if feature_info.check(str(secend_sentence[j])) is False:
                    test_strpuc[i][j][0] = 1
                else:
                    test_strpuc[i][j][0] = 0
        for j in range(sent_len):
            if j < 60:
                if feature_info.ifPunc(str(secend_sentence[j])) is True:
                    test_strpuc[i][j][1] = 1
                else:
                    test_strpuc[i][j][1] = 0
    return train_strpunc,test_strpuc
def read_ren_feature_list(train_path,vali_path,num):
    train_ren_feature = np.zeros(shape=(12000, 60, num))
    test_ren_feature = np.zeros(shape=(3000, 60, num))
    train_length = len(train_path)
    vali_length = len(vali_path)
    for i in range(train_length):
        pre_feature = train_path[i]
        length = len(pre_feature[0])
        for j in range(length):
            if j < 60:
                train_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
            else:
                continue
    for i in range(vali_length):
        pre_feature = vali_path[i]
        length = len(pre_feature[0])
        for j in range(length):
            if j < 60:
                test_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
            else:
                continue

    return train_ren_feature, test_ren_feature


def read_ren_feature(train_path,vali_path,num):
    train_ren_feature = np.zeros(shape=(12000,60,num))
    test_ren_feature = np.zeros(shape=(3000,60,num))

    with open(train_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature[0])
            for j in range(length):
                if j<60:
                    train_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
                else:
                    continue
    with open(vali_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature[0])
            for j in range(length):
                if j<60:
                    test_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
                else:
                    continue

    return train_ren_feature,test_ren_feature

def read_first_secend_feature_list(train_path,vali_path,num,jieba):
    train_ren_feature = np.zeros(shape=(num, 60, jieba))
    test_ren_feature = np.zeros(shape=(num, 60, jieba))
    train_length = len(train_path)
    vali_length = len(vali_path)
    for i in range(train_length):
        pre_feature = train_path[i]
        length = len(pre_feature[0])
        for j in range(length):
            if j < 60:
                train_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
            else:
                continue
    for i in range(vali_length):
        pre_feature = vali_path[i]
        length = len(pre_feature[0])
        for j in range(length):
            if j < 60:
                test_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
            else:
                continue

    return train_ren_feature, test_ren_feature


def read_first_secend_feature(train_path,vali_path,num,jieba):
    train_ren_feature = np.zeros(shape=(num,60,jieba))
    test_ren_feature = np.zeros(shape=(num,60,jieba))
    with open(train_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature[0])
            for j in range(length):
                if j<60:
                    train_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
                else:
                    continue
    with open(vali_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            pre_feature = json.loads(lines[i])
            length = len(pre_feature[0])
            for j in range(length):
                if j<60:
                    test_ren_feature[i][j] = np.array(pre_feature[0][j][1:]).flatten()
                else:
                    continue

    return train_ren_feature,test_ren_feature


def train_test_dic(train_sentences,vali_sentences):
    dits = []
    for train_sentence in train_sentences:
        for char in train_sentence:
            if char not in dits:
                dits.append(char)
    for vali_sentence in vali_sentences:
        for char in vali_sentence:
            if char not in dits:
                dits.append(char)
    return dits

def read_search_feature():
    url_train = "../data/add_feature"
    url_vali = "../data/vali_add_feature_4"

    with  open(url_train,"r",encoding="utf-8") as f:
        train_search_features = json.load(f)
    with  open(url_vali,"r",encoding="utf-8") as f:
        vali_search_features = json.load(f)
    return train_search_features,vali_search_features

def read_sent_length(sentences):
    sent_feature = []
    for sentence in sentences:
        sent_feature.append(len(sentence))
    sent_feature = np.array(sent_feature)
    return sent_feature

def read_first_sencend(first_secend,num):
    first_length = []
    secend_length = []
    for i in range(num):
        fisrt_sentence = first_secend[i].strip().split("\t")[0]
        secend_sentence = first_secend[i].strip().split("\t")[1]
        first_length.append(len(fisrt_sentence))
        secend_length.append(len(secend_sentence))
    first_length = np.array(first_length)
    secend_length = np.array(secend_length)
    return first_length,secend_length



def read_vec_index(first_secend,dit,bag_of_word,n1):
    max_text_word = 60
    first_index = np.zeros((n1,max_text_word),dtype=np.int32)
    secend_index = np.zeros((n1,max_text_word),dtype=np.int32)
    for i in range(0, n1):
        # z = x_train[i]
        fisrt_sentence = first_secend[i].strip().split("\t")[0]
        #sencend_sentence = first_secend[i].strip().split("\t")[1]
        lenth = len(fisrt_sentence)
        for j in range(max_text_word):
            if j < lenth:
                if fisrt_sentence[j] not in dit.keys():
                    first_index[i, j] = len(dit)
                else:
                    first_index[i, j] = bag_of_word.index(fisrt_sentence[j])
            else:
                first_index[i, j] = len(dit)
    for i in range(0, n1):
        secend_sentence = first_secend[i].strip().split("\t")[1]
        lenth = len(secend_sentence)
        for j in range(max_text_word):
            if j < lenth:
                if secend_sentence[j] not in dit.keys():
                    secend_index[i, j] = len(dit)
                else:
                    secend_index[i, j] = bag_of_word.index(secend_sentence[j])
            else:
                secend_index[i, j] = len(dit)
    return first_index,secend_index

def model_predict(model,first_feature,secend_feature):
    #model = load_model(model_path)
    test_first_label = model.predict(first_feature,batch_size=64)
    test_secend_label = model.predict(secend_feature,batch_size=64)
    test_first_label = to_categorical(np.argmax(test_first_label,axis=-1))
    test_secend_label = to_categorical(np.argmax(test_secend_label, axis=-1))
    return test_first_label,test_secend_label


#train_path最后一句话,test_path测试集最后一句话,
def reClassLabel(train_path,test_path,fisrt_path,secend_path,test_fisrt_path,test_secend_path,wurl,leng):

        album_train_label = feature_info.read_artist_feature_list(train_path ,12000)
        artist_train_label = feature_info.read_album_feature_list(train_path ,12000)
        genre_train_label = feature_info.read_genre_feature_list(train_path, 12000)
        song_train_label = feature_info.read_song_feature_list(train_path ,12000)

        artist_test_label = feature_info.read_artist_feature_list(test_path,3000)
        album_test_label = feature_info.read_album_feature_list(test_path,3000)
        song_test_label = feature_info.read_song_feature_list(test_path,3000)
        genre_test_label = feature_info.read_genre_feature_list(test_path,3000)

        # fisrt_path = "../data/特征信息/first_sent_feature_train_genre_nojieba"
        # secend_path = "../data/特征信息/second_sent_feature_train_genre_nojieba"
        # test_fisrt_path = "../data/特征信息/first_sent_feature_test_genre_nojieba"
        # test_secend_path = "../data/特征信息/second_sent_feature_test_genre_nojieba"

        fisrt_artist_label = feature_info.read_artist_feature_list(fisrt_path,12000)
        fisrt_album_label = feature_info.read_album_feature_list(fisrt_path, 12000)
        fisrt_song_label = feature_info.read_song_feature_list(fisrt_path, 12000)
        fisrt_genre_label = feature_info.read_genre_feature_list(fisrt_path, 12000)

        secend_artist_label = feature_info.read_artist_feature_list(secend_path, 12000)
        secend_album_label = feature_info.read_album_feature_list(secend_path, 12000)
        secend_song_label = feature_info.read_song_feature_list(secend_path, 12000)
        secend_genre_label = feature_info.read_genre_feature_list(secend_path, 12000)

        test_fisrt_artist_label = feature_info.read_artist_feature_list(test_fisrt_path, 3000)
        test_fisrt_album_label = feature_info.read_album_feature_list(test_fisrt_path, 3000)
        test_fisrt_song_label = feature_info.read_song_feature_list(test_fisrt_path, 3000)
        test_fisrt_genre_label = feature_info.read_genre_feature_list(test_fisrt_path, 3000)

        test_secend_artist_label = feature_info.read_artist_feature_list(test_secend_path, 3000)
        test_secend_album_label = feature_info.read_album_feature_list(test_secend_path, 3000)
        test_secend_song_label = feature_info.read_song_feature_list(test_secend_path, 3000)
        test_secend_genre_label = feature_info.read_genre_feature_list(test_secend_path, 3000)

        url = r'data/train.txt'
        ur2 = r"data/t2_test_set.txt"

        last,fisrt_secend = vectsent.readContent(url)
        test_first_secend = readtestData(ur2)
        train_strpuc, test_strpuc = feature_info.readcheckpunc(url, ur2)
        first_strpuc, secend_strpuc = readcheckpunc_first_secend(fisrt_secend,12000)
        test_first_strpuc,test_secend_strpuc = readcheckpunc_first_secend(test_first_secend,3000)



        x_test = []
        valiallsents = vectsent.readValidData(ur2)
        for i in range(len(valiallsents)):
            x_test.append(valiallsents[i][1][1:])
        lastsents = []
        label_3 = class_8_10.readlabel_4(url)
        label_3 = to_categorical(label_3)

        for i in range(len(last)):
              lastsents.append(last[i][0])

        train_ren_feature,test_ren_feature = read_ren_feature_list(train_path,test_path,leng)
        fiset_ren_feature,secend_ren_feature = read_first_secend_feature_list(fisrt_path,secend_path,12000,leng)
        test_first_ren_fearture,test_secend_ren_fearture = read_first_secend_feature_list(test_fisrt_path,test_secend_path,3000,leng)

        train_sent_len_feature = read_sent_length(lastsents)
        test_sent_len_feature = read_sent_length(x_test)
        first_length,secend_length = read_first_sencend(fisrt_secend,12000)
        test_first_length,test_secend_length = read_first_sencend(test_first_secend,3000)



        dit = {}
        with open("model/wiki.zh.text.vector_filter","r",encoding="utf-8") as f:
              for line in f.readlines():
                  key = line[0]
                  if key not in dit:
                       dit[key] = 1
                  else:
                       continue
        model = Word2Vec.load("model/wiki.zh.text.model")
        num_words = len(dit)
        bag_of_word = list(dit.keys())

        embedding_matrix = np.zeros((num_words+1,200))
        for i in range(len(dit)):
            embedding_matrix[i] =(model[bag_of_word[i]])


        fisrt_index,secend_index = read_vec_index(fisrt_secend ,dit,bag_of_word,12000)
        test_first_index,test_secend_index = read_vec_index(test_first_secend,dit,bag_of_word,3000)



        n1 = 12000
        n3 = 3000
        max_text_word = 60
        X_train = np.zeros((n1,max_text_word), dtype=np.int32)
        X_test = np.zeros((n3,max_text_word),dtype=np.int32)
        for i in range(0,n1):
            #z = x_train[i]
            z = lastsents[i]
            lenth = len(z)
            for j in range(max_text_word):
                if j<lenth:
                    if z[j] not in dit.keys():
                        X_train[i,j] = num_words
                    else:
                        X_train[i,j] = bag_of_word.index(z[j])
                else:
                    X_train[i, j] = num_words
        for i in range(0, n3):
            z = x_test[i]
            lenth = len(z)
            for j in range(max_text_word):
                if j < lenth:
                    if z[j] not in dit.keys():
                        X_test[i, j] = num_words
                    else:
                        X_test[i, j] = bag_of_word.index(z[j])
                else:
                    X_test[i, j] = num_words
        n_class = 3
        batch_size = 64
        epochs = 50
        embedding_layer = Embedding(num_words+1,200,weights=[embedding_matrix],input_length=60,trainable=False)



        #cnn
        sequence_input_1 = Input(shape=(60,), dtype='int32')
        sequence_input_2 = Input(shape=(3,),dtype="float32")
        sequence_input_2_1 = Input(shape=(3,),dtype="float32")
        sequence_input_3 = Input(shape=(60,16),dtype="float32") #ren 16维
        sequence_input_4 = Input(shape=(1,),dtype="float32")    #句子长度

        sequence_input_5 = Input(shape=(60,4),dtype="float32")   #artist ren
        sequence_input_6 = Input(shape=(60, 4), dtype="float32") #album ren
        sequence_input_7 = Input(shape=(60, 4), dtype="float32") #song  ren
        sequence_input_8 = Input(shape=(60, 4), dtype="float32") #genre ren
        sequence_input_9 = Input(shape=(60, 2),dtype="float32")  #strpuc
        embedded_sequences = embedding_layer(sequence_input_1)
        biaozhu = sequence_input_3
        artist = sequence_input_5
        album = sequence_input_6
        song = sequence_input_7
        genre = sequence_input_8
        strpuc = sequence_input_9

        embedded_sequences = concatenate([embedded_sequences,biaozhu,artist,album,song,genre,strpuc])
        embedded_sequences = Dropout(0.4)(embedded_sequences)

        x = Conv1D(256, 5, activation='relu')(embedded_sequences)
        x = MaxPooling1D(5)(x)

        x = Flatten()(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)


        #rnn:
        y = LSTM(128,dropout=0.3,recurrent_dropout=0.3)(embedded_sequences)

        z = sequence_input_2
        z_1 = sequence_input_2_1


        length = sequence_input_4
        #
        merges_1  = concatenate([x,y,length])
        merges_2 = concatenate([x,y,z,z_1,length])

        pred_1 = Dense(n_class,activation="softmax",kernel_regularizer=l1(0.005))(merges_1)
        pred_2 = Dense(n_class, activation="softmax", kernel_regularizer=l1(0.005))(merges_2)

        model_1 = Model(inputs=[sequence_input_1,sequence_input_3,sequence_input_4,
                                sequence_input_5,sequence_input_6,sequence_input_7,sequence_input_8,sequence_input_9],outputs=pred_1)
        model_2 = Model(inputs=[sequence_input_1,sequence_input_2,sequence_input_2_1, sequence_input_3, sequence_input_4,
                                sequence_input_5, sequence_input_6, sequence_input_7,sequence_input_8,sequence_input_9], outputs=pred_2)

        #编译模型
        model_1.compile(loss="categorical_crossentropy",
                      optimizer="adadelta",
                      metrics=["accuracy"])
        model_2.compile(loss="categorical_crossentropy",
                        optimizer="adadelta",
                        metrics=["accuracy"])

        model_1.fit([X_train,train_ren_feature,train_sent_len_feature,
                     artist_train_label,album_train_label,song_train_label,genre_train_label,train_strpuc],label_3,batch_size=batch_size,
                    epochs=epochs,verbose=1)
        first_label_1 = model_1.predict([fisrt_index,fiset_ren_feature,first_length,
                                       fisrt_artist_label,fisrt_album_label,fisrt_song_label,fisrt_genre_label,first_strpuc],batch_size=64)
        secend_label_1 = model_1.predict([secend_index, secend_ren_feature, secend_length,
                                       secend_artist_label, secend_album_label, secend_song_label,secend_genre_label,secend_strpuc],
                                      batch_size=64)
        first_label = np.argmax(first_label_1, axis=-1)
        secend_label = np.argmax(secend_label_1, axis=-1)
        first_label = to_categorical(first_label)
        secend_label = to_categorical(secend_label)

        model_2.fit([X_train, first_label,secend_label,train_ren_feature, train_sent_len_feature,
                     artist_train_label, album_train_label, song_train_label,genre_train_label,train_strpuc], label_3, batch_size=batch_size,
                    epochs=epochs, verbose=1)
        first_feature = [test_first_index,test_first_ren_fearture,test_first_length,test_fisrt_artist_label,test_fisrt_album_label,
                         test_fisrt_song_label,test_fisrt_genre_label,test_first_strpuc]
        secend_feature = [test_secend_index,test_secend_ren_fearture,test_secend_length,test_secend_artist_label,test_secend_album_label,
                         test_secend_song_label,test_secend_genre_label,test_secend_strpuc]

        test_first_label, test_secend_label = model_predict(model_1,first_feature,secend_feature)

        pred = model_2.predict([X_test,test_first_label,test_secend_label,test_ren_feature,test_sent_len_feature,
                                artist_test_label,album_test_label,song_test_label,genre_test_label,test_strpuc])

        final_label = np.argmax(pred, axis=-1)
        index = []

        for label in final_label:
            index.append(str(label))

        with open(wurl, "w",
                  encoding="utf-8") as f:
            json.dump(index, f)

        return index





