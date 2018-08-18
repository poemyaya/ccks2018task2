# -*- coding: utf-8 -*-
import string,json
from collections import Counter
def readContent(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
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

def ifPunc(puncstr):
    punc = string.punctuation
    punc = punc + '。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'
    return puncstr in punc

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


def reValueList(words,datadicts):
    reLists = []
    for char_i in range(len(words)):
        char = words[char_i]
        if char in datadicts.keys():
            values = datadicts[char]
            for char_j in range(char_i, len(words), 1):
                charlist = [words[i] for i in range(char_i, char_j + 1, 1)]
                name = ''.join(charlist)
                if name in values:
                    reLists.append(name)
    reLists = list(set(reLists))
    return reLists

def produPattern1(sent,valueList,typystr,slotvalue):
    pattern = []
    for item in valueList:
        ss = sent.replace(item,typystr)
        ifNorP = 'N'
        if typystr in list(slotvalue.keys()):
            if item in list(slotvalue[typystr]):
                ifNorP = 'P'
        pattern.append(ss + '\t' + typystr + '\t' + ifNorP)
    return pattern


def produPattern2(sent,valueList1,typystr1,valueList2,typystr2,slotvalue):
    pattern = []
    for item1 in valueList1:
        for item2 in valueList2:
            ifNorP = 'N'
            if typystr1 in list(slotvalue.keys()) and typystr2 in list(slotvalue.keys()):
                if item1 in list(slotvalue[typystr1]) and item2 in list(slotvalue[typystr2]):
                    ifNorP = 'P'
            if item1 in item2 or item2 in item1:
                continue
            ss = sent.replace(item1, typystr1)
            ss2 = ss.replace(item2, typystr2)
            pattern.append(ss2 + '\t' + typystr1 + '\t' + typystr2 + '\t' + ifNorP)
    return pattern


if __name__=='__main__':
    trainurl = 'data/train.txt'
    allSentsDicts = readContent(trainurl)
    albums = json.load(open(r'data/albums_hash.json', encoding='utf-8'))
    artist = json.load(open(r'data/singers_hash.json', encoding='utf-8'))
    songs = json.load(open(r'data/songs_hash.json', encoding='utf-8'))

    albumslists = []
    artistlists = []
    songslists = []
    # allSentsDicts = [['我要看我的车在哪里。']]
    allpattern = []

    for sentlist in allSentsDicts:
        sent = sentlist[0]
        slotvalue = sentlist[1]
        words = sentTochar(sent, func(resentrecord(sent)))
        songssent = reValueList(words, songs)
        albumssent = reValueList(words, albums)
        artistsent = reValueList(words, artist)
        # print(songssent)
        # print(albumssent)
        # print(artistsent)

        allpattern.extend(produPattern1(sent, songssent, 'song', slotvalue))
        allpattern.extend(produPattern1(sent, albumssent, 'album', slotvalue))
        allpattern.extend(produPattern1(sent, artistsent, 'artist', slotvalue))

        allpattern.extend(produPattern2(sent,songssent, 'song',albumssent, 'album',slotvalue))
        allpattern.extend(produPattern2(sent, songssent, 'song', artistsent, 'artist',slotvalue))
        allpattern.extend(produPattern2(sent, albumssent, 'album', artistsent, 'artist',slotvalue))

    # print(allpattern[:5])
    rules = {}
    rdict = Counter(allpattern)
    for r, f in rdict.items():
        # print(r)
        flag = r[-1]
        r = r[:-1]
        if r not in rules:
            rules[r] = [0, 0]

        if flag == 'P':
            rules[r][0] = f
        else:
            rules[r][1] = f
    # print(rules)

    suprules = []
    for r, freqs in rules.items():
        p = freqs[0]
        n = freqs[1]
        sup = p / (p+n)
        suprules.append((r, sup, p+n, p, n))
    suprules = sorted(suprules, key=lambda x: (-x[1], -x[2]))

    with open('data/suprules_filt', 'w', encoding='utf8') as f:
        for sr in suprules:
            if sr[1] >= 0.5:
                f.write('{}\t{}\t{}\t{}\n'.format(sr[0], sr[1], sr[2], sr[3], sr[4]))

