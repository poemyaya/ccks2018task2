import re
import json

def parse(line, state='train'):
    line = line.strip()
    # 句子编号
    sno = re.match('[0-9]+', line)
    # 分句
    pieces = re.split(r'[0-9:/\t\ ",]*', line)
    pieces = [p for p in pieces if len(p) > 0]
    sent_1 = pieces[0]
    sent_2 = pieces[1]
    sent_3 = pieces[2]
    flag = True  # 记录是否出错
    if state == 'train':
        # 槽值标注
        slotstr = re.findall(r"([{].*[}])$", line)[0]
        s2v = None
        try:
            s2v = json.loads(slotstr)
            s2v = dict(s2v)
        except:
            flag = False
            print(line)
        return (sent_1, sent_2, sent_3), s2v, flag
    else:
        return (sent_1, sent_2, sent_3), flag


if __name__=='__main__':
	dataset = []
	trainpath = 'data/train.txt'
	with open(trainpath, 'r', encoding='utf8') as f:
		for line in f.readlines():
			sents, s2v, flag  = parse(line)
			if flag:
				dataset.append((sents, s2v))


	keys = ['mood', 'genre', 'scene', 'language', 'tag']
	slotdict = {}
	for k in keys:
		slotdict[k] = []

	for _, s2v in dataset:
		for k in list(s2v.keys()):
			if k in keys:
				slotdict[k].append(s2v[k])
			
	for k in list(slotdict.keys()):
		slotdict[k] = set(slotdict[k])
	print(slotdict)


	for k, vs in slotdict.items():
		for v in vs:
			path = 'data/slotsamples/' + k + '_' + v
			with open(path, 'w', encoding='utf8') as f:
				for sents, s2v in dataset:
					ls = sents[-1]
					if k in s2v:
						if s2v[k] == v:
							f.write('P\t' + ls + '\t' + str(s2v) +'\n')
					else:
						if ls.find(v) > -1:
							f.write('N\t' + ls + '\t' + str(s2v) +'\n')

