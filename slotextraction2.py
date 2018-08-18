# song/album/artist
def readrules(path):
    rdict = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            pieces = line.strip().split('\t')
            rule = pieces[0]
            sup = pieces[-3]
            res = pieces[1:-3]
            if float(sup) >= 0.5:
                if rule in rdict:
                    rdict[rule].append(res)
                else:
                    rdict[rule] = res
    return rdict
rdict = readrules('data/suprules_filt')
# print(rdict.keys())


import string
import json
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



# 一阶规则
def apply(sent, typestr, values, rules):
    dummylist = {
        "song":['歌', '儿歌', '音乐', '唱歌', '点歌', '十', '听歌', '情歌', '电子', '吧', '放一首歌', '的歌',
                '唱首歌', '电子', '国家', '民谣', '亲', '世界', '唱儿歌', '呀', '哈啰', '的', '大', '成名曲',
               '相思', '童谣', '这首歌', '不知道不知道', '那个', '抒情', '大家好', '重新', '摇滚', '林宥嘉',
               '我的', '萨克斯', '相声', '周杰伦', '吉祥三宝', '我是你爸', '广场舞', '唱一首歌', '一首歌'],
        "artist":['我', '你' ,'传奇', '认真', '阿里山', '无言', '相思'],
        "album":['我', '请', '你' ,'听', '放', '大', '听天', '曲一', '听我']
    }
    result = []
    for v in values:
        vs = sent.replace(v, typestr)
        if vs in rules and typestr in rules[vs]:
            if v not in dummylist[typestr]:
                result.append('"{}":"{}"'.format(typestr, v))
    result = list(set(result))
    result = ','.join(result)
    return result


# 二阶规则
def rep(sent, vlist, tlist):
    result = sent
    flag = True
    pre = sent
    for v, t in zip(vlist, tlist):
        post = pre.replace(v, t)
        if pre == post:
            flag = False
            break
        else:
            pre = post
    result = post
    return result, flag


def apply2(sent, tstr1, values1, tstr2, values2, rules):
    dummylist = {
        "song":['歌', '儿歌', '音乐', '唱歌', '点歌', '十', '听歌', '情歌', '电子', '吧', '放一首歌', '的歌', 
                '唱首歌', '电子', '国家', '民谣', '亲', '世界', '唱儿歌', '呀', '哈啰', '的', '大', '成名曲',
               '相思', '舞曲', '我叫', '相声', '悦', '我的名字叫', '树', '一下', '人', '歌手', '唱一首歌', '一首歌'],
        "artist":['我', '你' ,'传奇', '认真', '阿里山', '无言', '相思', '月亮', '梁祝', '飘飘', '王子', '鸭子', '蜜蜜',
                 '白龙', '天女', '莲花', '高飞', '乖乖', '静', '明明', '飞', '恰恰', '小水', '东方', '无悔', '功夫', 
                  '熊猫', '三宝', '刚好', '天亮', '红尘', '舞', '何龙', '灯', '雪', '心心', '马兰', '九九', '追梦',
                  '新歌', '小睿'],
        "album":['我', '请', '你' ,'听', '放', '大', '听天', '曲一', '听我']
    }
    result = []
    values1 = [v for v in values1 if v not in dummylist[tstr1]]
    values2 = [v for v in values2 if v not in dummylist[tstr2]]
    for v1 in values1:
        for v2 in values2:
            if v1.find(v2) < 0 and v2.find(v1) < 0:
                vlist = [v1, v2]
                tlist = [tstr1, tstr2]
                rule, flag = rep(sent, vlist, tlist)
                if flag and rule in rules:
                    for v, t in zip(vlist, tlist):
                        if len(v) > 0:
                            result.append('"{}":"{}"'.format(t, v))
#     for v in values:
#         vs = sent.replace(v, typestr)
#         if vs in rules and typestr in rules[vs]:
#             if v not in dummylist[typestr]:
#                 result.append('"{}":"{}"'.format(typestr, v))
#     result = list(set(result))
#     result = ','.join(result)
    result = list(set(result))
    result = ','.join(result)
    return result


if __name__ == '__main__':
    # 加载数据
    albums = json.load(open('data/albums_hash.json', encoding='utf-8'))
    albumadd = ['爸爸去哪儿五']
    for a in albumadd:
        if a[0] in albums:
            albums[a[0]].append(a)
        else:
            albums[a[0]] = [a]
    # artists
    artist = json.load(open('./data/singers_hash.json', encoding='utf-8'))
    artistadd = ['Gala', '鞠婧祎', 'beyond', '雨馨', '天之大人', '缝纫机乐队', '庄心妍', '伍佰', '萧亚轩', '姜玉阳',
                 '苏运莹', '王岳伦', '黄风凯', '王俊凯', '后街男孩', '王婵娟', '周华健', '林宥嘉', '王馨悦', '维塔斯',
                 '萧正楠', '蔡依林', '何琦', 'Lady Gaga', 'rain', '叶一茜', '龚一', 'lilly wood', '席琳迪翁', '李健',
                 '吉祥三宝', '杨斌', '韩磊', '陈坤', '汪洙', '杨乃文', 'jewel', '彭丽媛']
    for a in artistadd:
        if a[0] in artist:
            artist[a[0]].append(a)
        else:
            artist[a[0]] = [a]
    # songs
    songs = json.load(open('./data/songs_hash.json', encoding='utf-8'))
    songadd = ['信仰之名', '小李', '权御天下', '星光下的记忆', '认真的雪', '阿里山的姑娘', '无言的结局', '相思的债', '亲亲宝贝', '光年之外',
               '一八七四', '青春修炼手册', '对不起谢谢', '告白气球', '后羿板的演员', '电话号码', '残酷月光', '社会摇', 'my dream',
               '温柔C over', '江南style', '选择', '安和桥', '都选c', '相信爱情', 'home', '美丽的新世界', '睫毛弯弯', '核心价值观',
               'hello', '我静静的看着你装逼', '共同渡过', '小苹果', 'my heart will go on', '广东十年爱情故事', '新传', '我是一条小青龙',
               '超级飞侠歌', '的士高', '朋友想你了', '凉凉', '今生有约', '九百九十九朵玫瑰', '数鸭子', '梅花鹿', '我爱爸爸我爱妈妈',
               'flame', '鸽子情缘', '恋爱100年', '拉大锯扯大锯', '绿岛小夜曲', '擎天', 'bad romance', '爱出发', '水木年华', '打靶归来',
               '爱拼才会赢', '黄鹂鸟', '小鸡小鸡', '大王叫我来巡山', '宝贝睡午觉', '无尽空虚', '小苹果', 'bingo', '带我去旅行',
               '传奇', '两只老虎', '山路18弯', '成都', '鸭子歌', '军港之夜', '小熊乐园', '江南style', '咖哩咖哩', '圣诞歌', '葫芦小金刚',
               'A BC D', '外婆故事', '贝瓦儿歌', '九九艳阳天']
    for s in songadd:
        if s[0] in songs:
            songs[s[0]].append(s)
        else:
            songs[s[0]] = [s]

    # 抽取槽值
    testpath = 'data/t2_test_set.txt'
    # respath1 = './data/test_result_1.txt'
    # resfile1 = open(respath1, 'w', encoding='utf8')
    respath2 = 'data/rules_lvl2.txt'
    resfile2 = open(respath2, 'w', encoding='utf8')
    with open(testpath, 'r', encoding='utf8') as f:
        for line in f:
            pieces = line.split(',"')
            sno = pieces[0]
            sent = pieces[-1].split('\t')[0]

            words = sentTochar(sent, func(resentrecord(sent)))
            # song
            songssent = reValueList(words, songs)
            # album
            albumssent = reValueList(words, albums)
            # artist
            artistsent = reValueList(words, artist)

            #             # 一阶规则抽取
            #             slt_song = apply(sent, 'song', songssent, rdict)
            #             slt_artist = apply(sent, 'album', albumssent, rdict)
            #             slt_album = apply(sent, 'artist', artistsent, rdict)
            #             slots = ','.join([slt_song, slt_artist, slt_album])
            #             resfile1.write('{}\t{}\t{}\n'.format(sno, sent, slots))

            # 二阶规则抽取
            slt_01 = apply2(sent, 'song', songssent, 'artist', artistsent, rdict)
            slt_12 = apply2(sent, 'song', songssent, 'album', albumssent, rdict)
            slt_02 = apply2(sent, 'album', albumssent, 'artist', artistsent, rdict)
            slots = ','.join([slt_01, slt_12, slt_02])
            resfile2.write('{}\t{}\t{}\n'.format(sno, sent, slots))

    # resfile1.close()
    resfile2.close()

