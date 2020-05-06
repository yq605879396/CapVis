##------------------------------------------##
# Use this code to generate caption analysis #
# based on the length of caption (Flickr-8K) #
##------------------------------------------##

import numpy as np
import pandas as pd

# load captions from the local file
f_captions = open('pretrained/all_caption.csv', 'r')
captions = f_captions.readlines()
for i in range(len(captions)):
    captions[i] = captions[i].strip('\n')
# load labels from the local file
labels = np.loadtxt('pretrained/labels_100')

#print("The size of labels:", labels.shape)
#print("The length of captions: %d" % (len(captions)))

Database = []
# each label corresponds to several lengths
Column = ['label', 'cap_length', 'number']

for i in range(100):
    dic = {}
    temp = 0
    for j in range(len(labels)):
        if labels[j] == i:
            temp += 1
            length = len(captions[j+1].split(' '))
            if length in dic:
                dic[length] += 1
            else:
                dic[length] = 1
    dic = sorted(dic.items(), key=lambda item:item[0])
    for j in range(len(dic)):
        # the third column stores the ratio
        Database.append([i, dic[j][0], dic[j][1]/temp])
    if (i+1) % 10 == 0:
        print("The %dth label finished!" % (i))

Export_Data = pd.DataFrame(columns=Column, data=Database)
Export_Data.to_csv('words_number.csv', index=False)