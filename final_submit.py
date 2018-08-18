# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     submit_data
   Description :
   Author :       sasuke
   date：          2018/7/17
-------------------------------------------------
   Change Activity:
                   2018/7/17:
-------------------------------------------------
"""
__author__ = 'sasuke'
import json
import re

def submit_data(read_path,mid_write_path_1,final_write_path_2,revise_path):
    F = open(mid_write_path_1, "w", encoding="utf-8")
    with open(read_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            result = {}
            line_split = line.strip().split("\t")
            id = line_split[0]
            sentence = line_split[1]
            # dict_1_str = json.loads(line_split[2])#5
            slot_5 = line_split[2]  #
            label = int(line_split[3])
            re.sub('\'', '\"', line_split[4])

            dict_2 = json.loads(line_split[4])  # 3
            filtRANDOM = ['播放', '音乐', '歌曲', '歌', '听', '唱', "首"]
            if slot_5 != "{}":
                if dict_2 == {}:
                    result = slot_5
                    F.write(id + "\t" + result.replace(":", ": ") + "\n")
                else:
                    new_label = []
                    str1 = ""
                    for key in dict_2:
                        value = dict_2[key]
                        if len(value) == 1:
                            new_label.append([key, value[0]])
                        else:
                            for i in range(len(value)):
                                new_label.append([key, value[i]])
                    for i in new_label:
                        str1 += "{"
                        str1 += '"'
                        str1 += i[0]
                        str1 += '"'
                        str1 += ':'
                        str1 += " "
                        str1 += '"'
                        str1 += i[1]
                        str1 += '"'
                        str1 += "}"
                        str1 += ","
                    str1 = re.sub('},{', ', ', str1)
                    str1 = str1[:-1]
                    str1 = str1[:-1] + ", " + slot_5[1:-1].replace(":", ": ") + "}"
                    F.write(id + "\t" + str1 + "\n")
            else:
                if label == 1:
                    result["code"] = "RANDOM"

                    F.write(id + "\t" + json.dumps(result, ensure_ascii=False) + "\n")
                if label == 2:
                    result["code"] = "No-music"
                    F.write(id + "\t" + json.dumps(result, ensure_ascii=False) + "\n")
                if label == 0:
                    if len(dict_2) == 0:
                        for filter in filtRANDOM:
                            if filter in sentence:
                                result["code"] = "RANDOM"
                        if "code" not in result.keys():
                            result["code"] = "No-music"
                        F.write(id + "\t" + json.dumps(result, ensure_ascii=False) + "\n")
                    else:
                        new_label = []
                        str1 = ""
                        for key in dict_2:
                            value = dict_2[key]
                            if len(value) == 1:
                                new_label.append([key, value[0]])
                            else:
                                for i in range(len(value)):
                                    new_label.append([key, value[i]])
                        for i in new_label:
                            str1 += "{"
                            str1 += '"'
                            str1 += i[0]
                            str1 += '"'
                            str1 += ':'
                            str1 += " "
                            str1 += '"'
                            str1 += i[1]
                            str1 += '"'
                            str1 += "}"
                            str1 += ","
                        str1 = re.sub('},{', ', ', str1)
                        str1 = str1[:-1]
                        F.write(id + "\t" + str1 + "\n")
    f.close()
    F.close()
    revise_lines = open(revise_path,"r",encoding="utf-8").readlines()
    f = open(mid_write_path_1,"r",encoding="utf-8")
    F = open(final_write_path_2,"w",encoding="utf-8")
    lines = f.readlines()
    revise_index = []
    revise_dict = []
    for revise_line in revise_lines:
        revise_line = json.loads(revise_line)
        revise_id = int(revise_line[0])
        slot = revise_line[2]
        revise_index.append(revise_id)
        revise_dict.append(slot)
    for line in lines:
        line_split = line.strip().split("\t")
        id = int(line_split[0])
        if id in revise_index:
            new_slot = revise_dict[revise_index.index(id)]
            new_label = []
            str1 = ""
            for key in new_slot:
                value = new_slot[key]
                if len(value) == 1:
                    new_label.append([key, value[0]])
                else:
                    for i in range(len(value)):
                        new_label.append([key, value[i]])
            for i in new_label:
                str1 += "{"
                str1 += '"'
                str1 += i[0]
                str1 += '"'
                str1 += ':'
                str1 += " "
                str1 += '"'
                str1 += i[1]
                str1 += '"'
                str1 += "}"
                str1 += ","
            str1 = re.sub('},{', ', ', str1)
            str1 = str1[:-1]
            F.write(str(id) + "\t" + str1 + "\n")
            continue
        else:
            dict = json.loads(line_split[1])
            if "song" in dict.keys() and "tag" in dict.keys() and "artist" in dict.keys() and "genre" in dict.keys():
                # print(line)
                break
            if "song" in dict.keys() and "tag" in dict.keys():
                if dict["song"] == dict["tag"]:
                    # print(line_split[0] + str(dict))
                    dict.pop("song")
                    F.write(str(id) + "\t" + json.dumps(dict, ensure_ascii=False) + "\n")
                    continue
            if "artist" in dict.keys() and "genre" in dict.keys():
                if dict["artist"] == dict["genre"]:
                    # print(line_split[0] + str(dict))
                    dict.pop("artist")
                    F.write(str(id) + "\t" + json.dumps(dict, ensure_ascii=False) + "\n")
                    continue

            F.write(line)


            #F.write(str(id) + "\t" + json.dumps(dict, ensure_ascii=False) + "\n")




# submit_data(r'../data/testpredict_test719_4_norevise',"1","2",r"../data/needrevise.txt")
# print()



