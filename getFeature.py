# -*- coding: utf-8 -*-
'''
得到pycrf需要的特征
'''
import string,jieba
jieba.load_userdict(r'data/slotvaluesaa')
#将句子转为字
def sentTochar(sent,unionlist):
    words = []
    for i in range(len(unionlist)):
        indexes = 0
        if i>0:
            for k in range(0,i,1):
                indexes = indexes + len(unionlist[k])
        if 1 in unionlist[i]:
            words.append(''.join([sent[j+indexes] for j in range(len(unionlist[i]))]))
        else:
            words.extend([sent[j+indexes] for j in range(len(unionlist[i]))])
    return words

def func(l):
    alllist = []
    start = 0
    for i in range(1, len(l)):
        if l[i-1] == l[i]:
            continue
        else:
            alllist.append(l[start:i])
            start = i
    alllist.append(l[start: len(l)])
    return alllist

def resentrecord(sent):
    sentRecord = []
    for w in sent:
        if w >= u'\u4e00' and w <= u'\u9fa5':
            sentRecord.append(0)
        elif ifPunc(w):
            sentRecord.append(0)
        elif w==' ':
            sentRecord.append(0)
        else:
            sentRecord.append(1)
    return sentRecord

def ifPunc(puncstr):
    punc = string.punctuation
    punc = punc + '。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'
    return puncstr in punc

def reVect(datadicts, words):
    #S\B\M\E
    sentVect = [[0] * 4 for i in range(len(words))]
    for char_i in range(len(words)):
        char = words[char_i]

        if char in datadicts.keys():
            values = datadicts[char]
            for char_j in range(char_i, len(words), 1):

                charlist = [words[i] for i in range(char_i, char_j + 1, 1)]
                name = ''.join(charlist)
                if name in values:
                    if len(charlist) == 1:
                        sentVect[char_i][0] = 1
                    elif len(charlist) == 2:
                        sentVect[char_i][1] = 1
                        sentVect[char_j][3] = 1
                    else:
                        sentVect[char_i][1] = 1
                        for k in range(char_i + 1, char_j, 1):
                            sentVect[k][2] = 1
                        sentVect[char_j][3] = 1
    return sentVect

def findindex(lists,string):
    indexes = []
    for i in range(len(lists)):
        if string==lists[i]:
            indexes.append(i)
    return indexes

def reIndex(alist,blist):
    blistindex = []
    for b in blist:
        bindex = findindex(alist, b)
        blistindex.append(bindex)
    if len(blistindex)==1:
        return blistindex[0]
    lastindex = 0
    lastindexlist = []
    recordll = 1
    for i in range(len(blistindex[0])):
        for j in range(1,len(blistindex),1):
            if blistindex[0][i] + j in blistindex[j]:
                lastindex = blistindex[0][i] + j
            else:
                recordll = 0
                break
        if recordll==1:
            if ''.join([alist[q] for q in range(lastindex-len(blist)+1,lastindex+1,1)]) == ''.join(blist):
                lastindexlist.append(lastindex)
    if len(lastindexlist)==0:
        lastindexlist.append(lastindex)
    lastindexlist = [k+1-len(blist) for k in lastindexlist]
    return lastindexlist

def reLabels(sent,words,slotInfoDict,types):
    wordlabel = ['O' for i in words]
    if types in list(slotInfoDict.keys()):
        value_lists = slotInfoDict[types]
        for value in value_lists:
            valuelist = sentTochar(value, func(resentrecord(value)))
            if value in sent:
                indexeslist = reIndex(words,valuelist)
                if len(valuelist)==1:
                    for indexes in indexeslist:
                        wordlabel[indexes] = 'S-' + types
                else:
                    for indexes in indexeslist:
                        wordlabel[indexes] = 'B-' + types
                        for i in range(indexes + 1, len(valuelist) + indexes - 1, 1):
                            wordlabel[i] = 'M-' + types
                        wordlabel[len(valuelist) + indexes - 1] = 'E-' + types
    return wordlabel

def reVectInfo(sents,albumsdict,artistdict,songsdict,types):
    allsentInfo = []
    for sentlist in sents:
        sentvectinfo = []
        sent = sentlist[0].strip()
        # print(sent)
        slotInfoDict = sentlist[1]
        words = sentTochar(sent, func(resentrecord(sent)))
        # jiebafeature = reJiebaFeature(sent, words)
        sentVectalbum = reVect(albumsdict, words)
        sentVectartist = reVect(artistdict, words)
        sentVectsongs = reVect(songsdict, words)
        wordlabel = reLabels(sent, words, slotInfoDict, types)
        # if len(jiebafeature)!=len(words) or len(sentVectalbum)!=len(words) or len(sentVectartist)!=len(words) or len(sentVectalbum)!=len(words):
        #     print('----------',sent)
        for w in range(len(words)):
            sentvectinfo.append(
                (words[w], sentVectalbum[w], sentVectartist[w], sentVectsongs[w], wordlabel[w]))
            # sentvectinfo.append((words[w],jiebafeature[w],sentVectalbum[w],sentVectartist[w],sentVectsongs[w],wordlabel[w]))
        allsentInfo.append(sentvectinfo)
    return allsentInfo

def getFeature_sent(sent,albumsdict,artistdict,songsdict):
    sentvectinfo = []
    sent = sent.strip()
    words = sentTochar(sent, func(resentrecord(sent)))
    # jiebafeature = reJiebaFeature(sent, words)
    sentVectalbum = reVect(albumsdict, words)
    sentVectartist = reVect(artistdict, words)
    sentVectsongs = reVect(songsdict, words)
    for w in range(len(words)):
        sentvectinfo.append(
            (words[w], sentVectalbum[w], sentVectartist[w], sentVectsongs[w]))
        # sentvectinfo.append(
        #     (words[w], jiebafeature[w], sentVectalbum[w], sentVectartist[w], sentVectsongs[w]))
    return sentvectinfo

#加了jieba特征分类
def reReplacesent(sent,unionlist):
    newword = []
    repword = []
    kk = 0
    for i in range(len(unionlist)):
        indexes = 0
        if i>0:
            for k in range(0,i,1):
                indexes = indexes + len(unionlist[k])
        if 1 in unionlist[i]:
            newword.append('X'+str(kk))
            kk = kk+1
            repword.append(''.join([sent[j+indexes] for j in range(len(unionlist[i]))]))
        else:
            newword.extend([sent[j+indexes] for j in range(len(unionlist[i]))])
    newsent = ''.join(newword)
    return newsent,repword

def reJiebaFeature(sent,words):
    # B\M\E\S
    replist = reReplacesent(sent, func(resentrecord(sent)))
    repSent = replist[0]
    repacestr = replist[1]
    jieba_word = jieba.lcut(repSent)
    for ji in range(len(jieba_word)):
        for i in range(len(repacestr)):
            if jieba_word[ji] == 'X' + str(i):
                jieba_word[ji] = repacestr[i]
    newword = []
    for ww in jieba_word:
        if ww != 'X':
            newword.append(ww)
    jieba_word = newword
    charjiebalist = []
    for jw in range(len(jieba_word)):
        jw_word = jieba_word[jw]
        jw_word_no = sentTochar(jw_word, func(resentrecord(jw_word)))
        b = len(charjiebalist)
        leng = len(jw_word_no)
        wordCut = [words[w + b] for w in range(leng)]
        if len(wordCut) == 1:
            charjiebalist.append([0, 0, 0, 1])
        elif len(wordCut) == 2:
            charjiebalist.append([1, 0, 0, 0])
            charjiebalist.append([0, 0, 1, 0])
        else:
            charjiebalist.append([1, 0, 0, 0])
            for p in range(1, leng - 1, 1):
                charjiebalist.append([0, 1, 0, 0])

            charjiebalist.append([0, 0, 1, 0])
    return charjiebalist

def getFeature_sent_jieba(sent,albumsdict,artistdict,songsdict):
    sentvectinfo = []
    sent = sent.strip()
    words = sentTochar(sent, func(resentrecord(sent)))
    jiebafeature = reJiebaFeature(sent, words)
    sentVectalbum = reVect(albumsdict, words)
    sentVectartist = reVect(artistdict, words)
    sentVectsongs = reVect(songsdict, words)
    for w in range(len(words)):
        # sentvectinfo.append(
        #     (words[w], sentVectalbum[w], sentVectartist[w], sentVectsongs[w]))
        sentvectinfo.append(
            (words[w], jiebafeature[w], sentVectalbum[w], sentVectartist[w], sentVectsongs[w]))
    return sentvectinfo

