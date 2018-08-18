# -*- coding: utf-8 -*-
import json
'''
根据rule2 判断哪些槽值需要修改
'''
def readOutput(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    allsents = []
    k=0
    for line in lines:
        itemdict = {}
        line = line.strip('\n').strip()
        if ''.join(line[-2:]) == ',,':
            k = k+1
            line = line[:-2]
        line = line.strip().split('\t')
        id = line[0]
        sent = line[1]
        if len(line)==3:
            attrstr = line[2].split(',')
            for item in attrstr:
                item = item.split(':')
                key = item[0][1:-1]
                value = item[1][1:-1]
                if key not in itemdict:
                    itemdict[key] = []
                itemdict[key].append(value)
        allsents.append([id,sent,itemdict])
    print(k)
    return allsents

def readallresult(url):
    lines = open(url, 'r', encoding='UTF-8').readlines()
    allsents = []
    for line in lines:
        line = line.strip('\n').strip()
        line = line.split('\t')
        id = line[0]
        sent = line[1]
        attr5 = line[2]
        label = line[3]
        attr3 = json.loads(line[4])
        allsents.append([id,sent,attr5,label,attr3])
    return allsents

def reRevise(url2,url3,wurl):
    # url2 = r'data/rules_lvl2.txt'
    rules2 = readOutput(url2)
    # url3 = r'data/result/result_1.txt'
    rendatas = readallresult(url3)
    needRevise = []
    for i in range(len(rendatas)):
        rules2data = rules2[i][-1]
        rendata = rendatas[i][-1]
        if 'artist' in rendata.keys() and 'song' in rendata.keys():
            if rendata['artist'] == rendata['song']:
                needRevise.append([rendatas[i][0],rules2[i][1],{'artist': rendata['artist']}])
                # print('相同---',rendata, rules2data, rules2[i][0], rules2[i][1], rendatas[i][-2])
        else:
            if rules2data!={} and len(rendata.keys())<2:
                needRevise.append([rendatas[i][0], rules2[i][1], rules2data])
                # print(rendata, rules2data, rules2[i][0], rules2[i][1], rendatas[i][-2])
    write = open(wurl, 'w', encoding='utf-8')
    # write = open(r'data\needrevise.txt','w',encoding='utf-8')
    for ii in needRevise:
        write.write(json.dumps(ii, ensure_ascii=False)+'\n')

# if __name__=='__main__':
#
#     url2 = r'data/rules_lvl2.txt'
#     rules2 = readOutput(url2)
#     url3 = r'data/result/result_1.txt'
#     rendatas = readallresult(url3)
#     needRevise = []
#     for i in range(len(rendatas)):
#         rules2data = rules2[i][-1]
#         rendata = rendatas[i][-1]
#         if 'artist' in rendata.keys() and 'song' in rendata.keys():
#             if rendata['artist'] == rendata['song']:
#                 needRevise.append([rendatas[i][0],rules2[i][1],{'artist': rendata['artist']}])
#                 # print('相同---',rendata, rules2data, rules2[i][0], rules2[i][1], rendatas[i][-2])
#         else:
#             if rules2data!={} and len(rendata.keys())<2:
#                 needRevise.append([rendatas[i][0], rules2[i][1], rules2data])
#                 # print(rendata, rules2data, rules2[i][0], rules2[i][1], rendatas[i][-2])
#     write = open(r'data\needrevise.txt','w',encoding='utf-8')
#     for ii in needRevise:
#         write.write(json.dumps(ii, ensure_ascii=False)+'\n')
#
