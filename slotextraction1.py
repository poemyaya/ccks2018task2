# 1.读入所有规则
import os
dirpath ='data/rules/'
files = os.listdir(dirpath)
files = [f for f in files if f.find('.') < 0]
print(files)

import json
rules = {}
for fname in files:
    rules[fname] = []
    with open(dirpath + fname, 'r', encoding='utf8') as f:
        for line in f:
            ir = json.loads(line.strip())
            rules[fname].append(ir)
# print(rules)


# 2.对规则进行循环
def extract(sent, rules):
    results = []
    for slot, vrules in rules.items():
        for vr in vrules:
            _v = vr['value']
            _ps = vr['P']
            _ns = vr['N']
            flag = True
            # 4.是否在 N 中
            for n in _ns:
                if sent.find(n) > -1:
                    flag = False
                    break
            # 5.是否在 P 中
            if flag:
                for p in _ps:
                    if sent.find(p) > -1:
                        results.append('"{}":"{}"'.format(slot, _v))
                        break
    return '{{{}}}'.format(','.join(results))

# sent = '粤语。'
# print(extract(sent, rules))


testpath = 'data/t2_test_set.txt'
respath = 'data/closeattr_rule.txt'
resfile = open(respath, 'w', encoding='utf8')
with open(testpath, 'r', encoding='utf8') as f:
    for line in f:
        pieces = line.split(',"')
        sno = pieces[0]
        sent = pieces[-1].split('\t')[0]
#         print(sno)
#         print(sent)
        slots = extract(sent, rules)
        resfile.write('{}\t{}\t{}\n'.format(sno, sent, slots))
resfile.close()


