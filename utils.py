import os, io, time, json
import numpy as np
import nltk

# get current path in you computer
current_path = os.getcwd()

# define the path: these files are trained of line
# related codes are in usefule_code directory
Labels = np.loadtxt('./pretrained/labels_100')
All_vec = np.loadtxt('./pretrained/All_vectors')
Centers = np.loadtxt('./pretrained/center_100')
test_vec = np.loadtxt('uploaded_image/test_photo_vec')
f_caption = open('./pretrained/all_caption.csv', 'r')



caption_lines = f_caption.readlines()

tempt_seq=""  
tempt_seq_clear ="" 
tempt_caption_list = [] 
tempt_caption_words=[] 
tempt_total_words=[] 
tempt_catg_num = 0



for i in range(len(caption_lines)):
    caption_lines[i] = caption_lines[i].strip('\n')

def get_label(image_vector):
    min_dis = float('Inf')
    index = None
    for i in range(len(Centers)):
        dis = np.sum((image_vector - Centers[i])**2)
        if dis < min_dis:
            min_dis = dis
            index = i
    return index

def get_top_images(index, image_vector, k=5):
    result_index = []
    for i in range(len(Labels)):
        if Labels[i] == index:
            result_index.append(i+1)
    result_index_dis = []

    for i in range(len(result_index)):
        dis = np.sum((image_vector - All_vec[result_index[i]-1])**2)
        result_index_dis.append(dis)
    result_index_dis = np.array(result_index_dis)
    sorted_index = result_index_dis.argsort()

    result = []
    for i in range(k):
        result.append(result_index[sorted_index[i]])
    return result

def add_caption(image_list):
    result = []
    for i in range(len(image_list)):
        result.append(caption_lines[image_list[i]])
    return result

def word_static(index):
    result_index = []
    for i in range(len(Labels)):
        if Labels[i] == index:
            result_index.append(i+1)
    dic_num = {}
    dic_tag = {}

    #not_consider = ['a', 'in', 'of', 'the', 'on']
    #dic_ratio = {}
    for i in range(len(result_index)):
        cap_temp = caption_lines[result_index[i]]
        words = cap_temp.split(' ')
        word_tag = nltk.pos_tag(words)
        for j in range(len(word_tag)):
            if word_tag[j][1] in dic_tag:
                dic_tag[word_tag[j][1]] += 1
            else:
                dic_tag[word_tag[j][1]] = 1
        for j in range(len(words)):
            if words[j] in dic_num:
                dic_num[words[j]] += 1
            else:
                dic_num[words[j]] = 1
    total_words = sum(dic_num.values())
    dic_num = sorted(dic_num.items(), key=lambda item:item[1], reverse=True)
    dic_array = np.array(dic_num)

    labels = []
    X = []
    dump_data_1 = []
    for i in range(24):
        labels.append(dic_array[i][0])
        X.append(int(dic_array[i][1]))
    labels.append('others')
    temp = sum(X)
    X.append(total_words-temp)
    for i in range(len(labels)):
        dic_temp = {}
        dic_temp["name"] = labels[i]
        dic_temp["value"] = X[i]
        dump_data_1.append(dic_temp)
    fw_1 = open('static/show_as_website/text/pic_frequency.json', 'w')
    json.dump(dump_data_1, fw_1)

    tag_name = []
    tag_num = []
    dump_data_2 = []
    result_temp = 0
    dic_tag = sorted(dic_tag.items(), key=lambda item:item[1], reverse=True)
    for i in range(len(dic_tag)):
        if i<9:
            tag_name.append(dic_tag[i][0])
            tag_num.append(dic_tag[i][1])
        else:
            result_temp += dic_tag[i][1]
    tag_name.append('others')
    tag_num.append(result_temp)
    for i in range(len(tag_name)):
        dic_temp = {}
        dic_temp["name"] = tag_name[i]
        dic_temp["value"] = tag_num[i]
        dump_data_2.append(dic_temp)
    fw_2 = open('static/show_as_website/text/pic_tag.json', 'w')
    json.dump(dump_data_2, fw_2)

    return dic_num, total_words, dic_array.shape[0], len(dic_tag)


# used for mask image
def generate_new_image(can_w,can_h,x,y,w,h,img):

    # since the visualize image on web may zoom original image
    # we need to compute the location of original image
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)

    raw_w,raw_h = img.shape[1],img.shape[0]
    ratio_w, ratio_h = float(raw_w)/float(can_w), float(raw_h)/float(can_h)
    
    x = int(x*ratio_w)
    y = int(y*ratio_h)
    w = int(w*ratio_w)
    h = int(h*ratio_h)

    for i in range(h):
        for j in range(w):
            img[i+y][x+j] =[0,0,0]

    return img