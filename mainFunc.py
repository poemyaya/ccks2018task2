# -*- coding: utf-8 -*-
import json
import pycrfTrain,getFeature,testCrfModel,CNN_textclassfier,get_slotvalue
import final_submit,Rules2toRevise
import sys,os
import jieba,pycrfsuite
def readContent(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    # lines = lines[int(len(lines)*0.7):]
    allsentsDict = []
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
        a = labelString.split(',')
        slotvalue = {}
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

            if la in slotvalue:
                slotvalue[la].append(attrvalue)
            else:
                slotvalue[la] = [attrvalue]
        allsentsDict.append([lastStr,slotvalue])
    return allsentsDict

#read 训练集一二句句子
def readContent_train12(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    sentf = []
    sents = []
    for line in lines:
        line = line.strip('\n').strip()
        lineSplit = line.split(',{')
        if len(lineSplit) != 2:
            print(line)
        textString = lineSplit[0]
        labelString = lineSplit[1]
        textStringSplit = textString.split('","')
        if len(textStringSplit)==3:
            firstSent = textStringSplit[0].split(',"')[-1].split('\t')[0].strip()
            secondSent = textStringSplit[1].split('\t')[0].strip()
            sentf.append(firstSent)
            sents.append(secondSent)
        else:
            print('error')
    return sentf,sents

def gettestsent(sent):
    lastsent = sent.split('\t')[0]
    if lastsent[0] == '"':
        lastsent = lastsent[1:]
    return lastsent.strip().lower()

def readTestData(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    sent1 = []
    sent2 = []
    sent3 = []
    for line in lines:
        line = line.strip('\n').strip()
        line = line.split(',')
        id = line[0]
        textStringSplit = line[1:]
        if len(textStringSplit)==3:
            firstSent = gettestsent(textStringSplit[0])
            secondSent = gettestsent(textStringSplit[1])
            lastSent = gettestsent(textStringSplit[2])
            sent1.append(firstSent)
            sent2.append(secondSent)
            sent3.append(lastSent)
        else:
            print('error')

    return sent1,sent2,sent3

def readTesttoPred(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    allsents = []
    for line in lines:
        itemsent = []
        line = line.strip('\n').strip()
        line = line.split(',')
        id = line[0]
        itemsent.append(id)
        strString = line[1:]
        for item in strString:
            itemsent.append( gettestsent(item))
        allsents.append(itemsent)
    return allsents

def modelTofile(attr, train_sents):
     pycrfTrain.saveModel(attr, train_sents)

def againDealslotvalue(sent,artistDicts,valuesDict):
    if sent[-1] =='。':
        value = sent[:-1]
        if len(value) == 2:
            if value[0] == value[1]:
                return valuesDict
        firstwo = value[0]
        if firstwo in artistDicts:
            if value in artistDicts[firstwo]:
                valuesDict[list(valuesDict.keys())[0]].append(value)
    return valuesDict

def dict3slotvalue(datalist,sent,valuesDict):
    if len(list(valuesDict.values())[0]) != 0:
        return valuesDict
    words = jieba.lcut(sent, cut_all=False)
    for wo in words:
        if wo in datalist and wo not in list(valuesDict.values())[0]:
            valuesDict[list(valuesDict.keys())[0]].append(wo)
    return valuesDict

def predTest(closeattr_info,classfi_label,testSents,albums, artist, songs,taggerartist,taggeralbum,taggersongs,
             artistslot,albumsslot,songsslot,predicturl):
    # allpre_results = []
    wurl = open(predicturl, 'w', encoding='utf-8')
    for i in range(len(testSents)):
        id = testSents[i][0]
        # if i != 275:
        #     continue
        sent = testSents[i][-1]
        xmdatalist = closeattr_info[i]
        if id != xmdatalist[0]:
            print('error id')

        xm5Dict = xmdatalist[1]
        ydmLabel = classfi_label[i]

        sentFeture = getFeature.getFeature_sent(sent, albums, artist, songs)
        artistPrec = testCrfModel.predCrfModel(taggerartist, sentFeture, 'artist')
        albumPrec = testCrfModel.predCrfModel(taggeralbum, sentFeture, 'album')
        songPrec = testCrfModel.predCrfModel(taggersongs, sentFeture, 'song')

        unionpredslot = {}
        if len(artistPrec) > 0 and len(list(artistPrec.values())[0]) > 0:
            unionpredslot[list(artistPrec.keys())[0]] = artistPrec[list(artistPrec.keys())[0]]
        if len(albumPrec) > 0 and len(list(albumPrec.values())[0]) > 0:
            unionpredslot[list(albumPrec.keys())[0]] = albumPrec[list(albumPrec.keys())[0]]
        if len(songPrec) > 0 and len(list(songPrec.values())[0]) > 0:
            unionpredslot[list(songPrec.keys())[0]] = songPrec[list(songPrec.keys())[0]]

        #如果没有预测值再预测：如果槽值是一个（歌手。）且该歌手在歌手库中

        if len(unionpredslot) == 0:
            artistPrec = againDealslotvalue(sent, artist, artistPrec)
            if len(artistPrec) > 0 and len(list(artistPrec.values())[0]) > 0:
                unionpredslot[list(artistPrec.keys())[0]] = artistPrec[list(artistPrec.keys())[0]]

        if len(unionpredslot) == 0:
            artistPrec = dict3slotvalue(artistslot, sent, artistPrec)
            albumPrec = dict3slotvalue(albumsslot, sent, albumPrec)
            songPrec = dict3slotvalue(songsslot, sent, songPrec)

            if len(artistPrec) > 0 and len(list(artistPrec.values())[0]) > 0:
                unionpredslot[list(artistPrec.keys())[0]] = artistPrec[list(artistPrec.keys())[0]]
            if len(albumPrec) > 0 and len(list(albumPrec.values())[0]) > 0:
                unionpredslot[list(albumPrec.keys())[0]] = albumPrec[list(albumPrec.keys())[0]]
            if len(songPrec) > 0 and len(list(songPrec.values())[0]) > 0:
                unionpredslot[list(songPrec.keys())[0]] = songPrec[list(songPrec.keys())[0]]

        #一些过滤方式
        if len(unionpredslot) == 0:
            if '主题曲' in sent:
                unionpredslot['song'] = [sent[:-1]]
                # print('主题曲----', unionpredslot, ydmLabel)
            if '，' in sent:
                sentlist = sent.split('，')
                if '唱一首' in sentlist[0]:
                    unionpredslot['song'] = [sentlist[1][:-1]]
                    # print('唱一首----', unionpredslot, ydmLabel, sent)
            if '放' == sent[0]:
                songname = sent[1:-1]
                if songname in songs[songname[0]]:
                    unionpredslot['song'] = [songname]
                    # print('放----', unionpredslot, ydmLabel, sent)
        # allpre_results.append([id,sent,xm5Dict,ydmLabel,unionpredslot])
        wurl.write(str(id)+"\t")
        wurl.write(sent + "\t")
        wurl.write(xm5Dict + "\t")
        wurl.write(ydmLabel + "\t")
        wurl.write(json.dumps(unionpredslot, ensure_ascii=False) + '\n')
    # return allpre_results
def readClosefile(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    xmDatas = []
    for line in lines:
        line = line.strip('\n').split('\t')
        id = line[0]
        sent = line[1]
        attr = line[2]
        xmDatas.append([id,attr])
    return xmDatas
jieba.load_userdict(r'data/slotvaluesaa')

if __name__=='__main__':
    trainurl = 'data/train.txt'
    testurl = 'data/t2_test_set.txt'
    # 得到albums、artist、songs外部数据
    albums = json.load(open(r'data/albums_hash.json', encoding='utf-8'))
    artist = json.load(open(r'data/singers_hash.json', encoding='utf-8'))
    songs = json.load(open(r'data/songs_hash.json', encoding='utf-8'))

    allSentsDicts = readContent(trainurl)
    # print(sys.argv)
    if len(sys.argv) == 3:
        print('Using the existing models ')
        #直接使用训练好的模型
        albumModel = r'model/album_crfModel'
        artistModel = r'model/artist_crfModel'
        songsModel = r'model/songs_crfModel'
        genreModel = r'model/genre_crfModel'

        taggeralbum = pycrfsuite.Tagger()
        taggeralbum.open(albumModel)
        taggerartist = pycrfsuite.Tagger()
        taggerartist.open(artistModel)
        taggersongs = pycrfsuite.Tagger()
        taggersongs.open(songsModel)
        taggergenre = pycrfsuite.Tagger()
        taggergenre.open(genreModel)

        #提交结果最好的分类结果
        classfi_labels_url = "data/test_label_3.json"
        classfi_labels = json.load(open(classfi_labels_url))

    elif sys.argv[1] == '--classify':
        print('Training the classify model ')
        albumModel = r'model/album_crfModel'
        artistModel = r'model/artist_crfModel'
        songsModel = r'model/songs_crfModel'
        genreModel = r'model/genre_crfModel'

        taggeralbum = pycrfsuite.Tagger()
        taggeralbum.open(albumModel)
        taggerartist = pycrfsuite.Tagger()
        taggerartist.open(artistModel)
        taggersongs = pycrfsuite.Tagger()
        taggersongs.open(songsModel)
        taggergenre = pycrfsuite.Tagger()
        taggergenre.open(genreModel)

        sents1_train,sents2_train = readContent_train12(trainurl)
        first_sent_feature_train = testCrfModel.\
            writeSentToVect(sents1_train,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        second_sent_feature_train = testCrfModel.\
            writeSentToVect(sents2_train,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        last_sent_feature_train = testCrfModel.writeSentToVect_Train_lastsent(allSentsDicts,albums, artist, songs)


        sents1_test, sents2_test, sents3_test = readTestData(testurl)
        first_sent_feature_test = testCrfModel.\
            writeSentToVect(sents1_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        second_sent_feature_test = testCrfModel.\
            writeSentToVect(sents2_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        last_sent_feature_test = testCrfModel.\
            writeSentToVect(sents3_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        #路径为 存储预测标签 最后一个参数是传入向量长度 16是用了jieba的信息 12是没用的
        classfi_labels_url = "data/classify_label_jieba.json"

        classfi_labels = CNN_textclassfier.\
            reClassLabel(last_sent_feature_train, last_sent_feature_test, first_sent_feature_train, second_sent_feature_train,
                         first_sent_feature_test, last_sent_feature_test,classfi_labels_url,16)

    elif sys.argv[1] == '--pycrf':
        print('Training the sequence labeling model ')

        #保存albums、artist、songs的crf模型
        albumTrain = getFeature.reVectInfo(allSentsDicts,albums,artist,songs,'album')
        artistrain = getFeature.reVectInfo(allSentsDicts, albums,artist,songs, 'artist')
        songsTrain = getFeature.reVectInfo(allSentsDicts, albums, artist, songs, 'song')
        genreTrain = getFeature.reVectInfo(allSentsDicts, albums, artist, songs, 'genre')

        modelTofile('album', albumTrain)
        modelTofile('artist', artistrain)
        modelTofile('songs', songsTrain)
        modelTofile('genre', genreTrain)

        albumModel = r'model/album_crfModel'
        artistModel = r'model/artist_crfModel'
        songsModel = r'model/songs_crfModel'
        genreModel = r'model/genre_crfModel'

        taggeralbum = pycrfsuite.Tagger()
        taggeralbum.open(albumModel)
        taggerartist = pycrfsuite.Tagger()
        taggerartist.open(artistModel)
        taggersongs = pycrfsuite.Tagger()
        taggersongs.open(songsModel)
        taggergenre = pycrfsuite.Tagger()
        taggergenre.open(genreModel)

        #提交结果最好的分类结果
        classfi_labels_url = "data/test_label_3.json"
        classfi_labels = json.load(open(classfi_labels_url))
    elif sys.argv[1] == '--all':
        print('Training the sequence labeling model and the classify model')
        print('---sequence labeling model start---')
        #保存albums、artist、songs的crf模型
        albumTrain = getFeature.reVectInfo(allSentsDicts,albums,artist,songs,'album')
        artistrain = getFeature.reVectInfo(allSentsDicts, albums,artist,songs, 'artist')
        songsTrain = getFeature.reVectInfo(allSentsDicts, albums, artist, songs, 'song')
        genreTrain = getFeature.reVectInfo(allSentsDicts, albums, artist, songs, 'genre')

        modelTofile('album', albumTrain)
        modelTofile('artist', artistrain)
        modelTofile('songs', songsTrain)
        modelTofile('genre', genreTrain)

        albumModel = r'model/album_crfModel'
        artistModel = r'model/artist_crfModel'
        songsModel = r'model/songs_crfModel'
        genreModel = r'model/genre_crfModel'

        taggeralbum = pycrfsuite.Tagger()
        taggeralbum.open(albumModel)
        taggerartist = pycrfsuite.Tagger()
        taggerartist.open(artistModel)
        taggersongs = pycrfsuite.Tagger()
        taggersongs.open(songsModel)
        taggergenre = pycrfsuite.Tagger()
        taggergenre.open(genreModel)
        print('----classify model----')
        sents1_train,sents2_train = readContent_train12(trainurl)
        first_sent_feature_train = testCrfModel.\
            writeSentToVect(sents1_train,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        second_sent_feature_train = testCrfModel.\
            writeSentToVect(sents2_train,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        last_sent_feature_train = testCrfModel.writeSentToVect_Train_lastsent(allSentsDicts,albums, artist, songs)


        sents1_test, sents2_test, sents3_test = readTestData(testurl)
        first_sent_feature_test = testCrfModel.\
            writeSentToVect(sents1_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        second_sent_feature_test = testCrfModel.\
            writeSentToVect(sents2_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        last_sent_feature_test = testCrfModel.\
            writeSentToVect(sents3_test,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre)
        #路径为 存储预测标签 最后一个参数是传入向量长度 16是用了jieba的信息 12是没用的
        classfi_labels_url = "data/classify_label_jieba.json"

        classfi_labels = CNN_textclassfier.\
            reClassLabel(last_sent_feature_train, last_sent_feature_test, first_sent_feature_train, second_sent_feature_train,
                         first_sent_feature_test, last_sent_feature_test,classfi_labels_url,16)

    if sys.argv[-2]!='-o':
        print('Output format error')
    else:
        submiturl = sys.argv[-1]
        print('----test predict----')
        predict_sents = readTesttoPred(testurl)

        #返回训练集中置信度比较高的槽值
        artistslot = get_slotvalue.retureSlotvalue('artist')
        albumsslot = get_slotvalue.retureSlotvalue('album')
        songsslot = get_slotvalue.retureSlotvalue('song')

        closeattr_info = readClosefile('data/closeattr_rule.txt')
        #返回结果，需要进一步处理，融合
        predTest(closeattr_info, classfi_labels, predict_sents, albums, artist, songs, taggerartist, taggeralbum,
                     taggersongs, artistslot, albumsslot, songsslot,r'data/result/result_1.txt')
        #根据规则2 得到需要修改的槽值
        Rules2toRevise.reRevise(r'data/rules_lvl2.txt', r'data/result/result_1.txt', r'data/needrevise.txt')
        #返回提交的格式
        final_submit.submit_data(r'data/result/result_1.txt','data/result/midfile.txt',submiturl
                                 ,'data/needrevise.txt')







