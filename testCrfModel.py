# -*- coding: utf-8 -*-
import getFeature
import re,string
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

def word2features(sent, idx):
    words = ['#', '#']
    # words.extend([w for w, _, _, _, _ in sent])
    words.extend([w for w, _, _, _ in sent])
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

def sent2tokens(sent):
    return [token for token, albuminfo, artistinfo, songinfo in sent]
    # return [token for token, jiebainfo, albuminfo, artistinfo, songinfo in sent]

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

def predCrfModel(tagger,sent,types):
    pred = reEntity(sent2tokens(sent), tagger.tag(sent2features(sent)), types)
    return pred

def writeSentToVect(sents,albums, artist, songs,taggerartist,taggeralbum,taggersongs,taggergenre):
    testFeature = []
    for sent in sents:
        sentInfo = []
        # sent = sentlist[1]
        sentFeature = getFeature.getFeature_sent(sent, albums, artist, songs)
        sentFeature_jieba = getFeature.getFeature_sent_jieba (sent, albums, artist, songs)
        artistPrec = taggerartist.tag(sent2features(sentFeature))
        albumPrec = taggeralbum.tag(sent2features(sentFeature))
        songPrec = taggersongs.tag(sent2features(sentFeature))
        genrePrec = taggergenre.tag(sent2features(sentFeature))
        sentInfo.append(sentFeature_jieba)
        # sentInfo.append(sentFeature)
        sentInfo.append({'artist':artistPrec})
        sentInfo.append({'album':albumPrec})
        sentInfo.append({'song':songPrec})
        sentInfo.append({'genre':genrePrec})
        # predictslotinfo = testSlotValue8.rePredict(sent, flitinfo, templates)
        testFeature.append(sentInfo)
    return testFeature

def writeSentToVect_Train_lastsent(sents,albums, artist, songs):
    validFeature = []
    for sentlist in sents:
        sentInfo = []
        sent = sentlist[0].strip()
        slotInfoDict = sentlist[1]
        sentFeature = getFeature.getFeature_sent_jieba(sent, albums, artist, songs)
        words = getFeature.sentTochar(sent, getFeature.func(getFeature.resentrecord(sent)))
        artistPrec = getFeature.reLabels(sent, words, slotInfoDict, 'artist')
        albumPrec = getFeature.reLabels(sent, words, slotInfoDict, 'album')
        songPrec = getFeature.reLabels(sent, words, slotInfoDict, 'song')
        genrePrec = getFeature.reLabels(sent, words, slotInfoDict, 'genre')
        sentInfo.append(sentFeature)
        sentInfo.append({'artist':artistPrec})
        sentInfo.append({'album':albumPrec})
        sentInfo.append({'song':songPrec})
        sentInfo.append({'genre':genrePrec})
        # predictslotinfo = testSlotValue8.rePredict(sent, flitinfo, templates)
        validFeature.append(sentInfo)
    return validFeature