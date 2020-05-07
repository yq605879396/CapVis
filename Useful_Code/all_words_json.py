import numpy as np
import json
import nltk

f_captions = open('pretrained/all_caption.csv', 'r')
captions = f_captions.readlines()
for i in range(len(captions)):
    captions[i] = captions[i].strip('\n')
labels = np.loadtxt('pretrained/labels_100')

#print("The size of labels:", labels.shape)
#print("The length of captions: %d" % (len(captions)))

'''
Json_all = {"name": "all_words", "children": []}
for i in range(100):
    dic_temp = {"name": str(i),  "children": []}
    Json_all['children'].append(dic_temp)
'''

#print(Json_all)

def find(child_list, target):
    for i in range(len(child_list)):
        if child_list[i]['name'] == target:
            return i
    return -1

'''
for i in range(100):
    word_num = {}
    total_words = 0
    for j in range(len(labels)):
        if labels[j] == i:
            words = captions[j+1].split(' ')
            total_words += len(words)
            for k in range(len(words)):
                if words[k] in word_num:
                    word_num[words[k]] += 1
                else:
                    word_num[words[k]] = 1
    words_have = word_num.keys()
    words_tag = nltk.pos_tag(words_have)

    for j in range(len(words_tag)):
        tag_name = words_tag[j][1]
        words_name = words_tag[j][0]
        words_num = word_num[words_name]
        words_ratio = words_num / total_words

        index = find(Json_all['children'][i]['children'], tag_name)

        if index == -1:
            Json_all['children'][i]['children'].append({"name": tag_name, "children": [{"name": words_name, "value": words_ratio}]})
        else:
            Json_all['children'][i]['children'][index]['children'].append({"name": words_name, "value": words_ratio})
    
    if (i+1) % 5 == 0:
        print("The %dth label finished!" % (i))
'''

intersted = [19, 46, 0, 51, 2, 47, 8, 11, 95]
Json_all = {"name": "all_words", "children": []}
for i in range(len(intersted)):
    dic_temp = {"name": str(intersted[i]),  "children": []}
    Json_all['children'].append(dic_temp)
Json_all['children'].append({"name": "others", "children": []})

for i in range(len(intersted)):
    word_num = {}
    #total_words = 0
    for j in range(len(labels)):
        if labels[j] == intersted[i]:
            words = captions[j+1].split(' ')
            #total_words += len(words)
            for k in range(len(words)):
                if words[k] in word_num:
                    word_num[words[k]] += 1
                else:
                    word_num[words[k]] = 1
    words_have = word_num.keys()
    words_tag = nltk.pos_tag(words_have)

    for j in range(len(words_tag)):
        tag_name = words_tag[j][1]
        words_name = words_tag[j][0]
        words_num = word_num[words_name]
        #words_ratio = words_num / total_words

        index = find(Json_all['children'][i]['children'], tag_name)

        if index == -1:
            Json_all['children'][i]['children'].append({"name": tag_name, "children": [{"name": words_name, "value": words_num}]})
        else:
            Json_all['children'][i]['children'][index]['children'].append({"name": words_name, "value": words_num})
    
    print("The %dth label finished!" % (i))

word_num = {}
#total_words = 0
for j in range(len(labels)):
    if labels[j] not in intersted:
        words = captions[j+1].split(' ')
        #total_words += len(words)
        for k in range(len(words)):
            if words[k] in word_num:
                word_num[words[k]] += 1
            else:
                word_num[words[k]] = 1
words_have = word_num.keys()
words_tag = nltk.pos_tag(words_have)

for j in range(len(words_tag)):
    tag_name = words_tag[j][1]
    words_name = words_tag[j][0]
    words_num = word_num[words_name]
    #words_ratio = words_num / total_words

    index = find(Json_all['children'][-1]['children'], tag_name)

    if index == -1:
        Json_all['children'][-1]['children'].append({"name": tag_name, "children": [{"name": words_name, "value": words_num}]})
    else:
        Json_all['children'][-1]['children'][index]['children'].append({"name": words_name, "value": words_num})


fw = open('static/text/words_all.json', 'w')
json.dump(Json_all, fw)