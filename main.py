from flask import Flask, Response, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
from caption import test_photo, test_photo_easy
from flask import make_response
import cv2 as cv
import io
import time
import numpy as np
import matplotlib.pyplot as plt
import nltk
import json
Labels = np.loadtxt('./pretrained/labels_100')
All_vec = np.loadtxt('./pretrained/All_vectors')
Centers = np.loadtxt('./pretrained/center_100')
test_vec = np.loadtxt('photo/test_photo_vec')
f_caption = open('./pretrained/all_caption.csv', 'r')
caption_lines = f_caption.readlines()

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
    fw_1 = open('static/text/pic_frequency.json', 'w')
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
    fw_2 = open('static/text/pic_tag.json', 'w')
    json.dump(dump_data_2, fw_2)

    return dic_num, total_words, dic_array.shape[0], len(dic_tag)
### Ended by Dongzi ###

### Added fot twist
def generate_new_image(can_w,can_h,x,y,w,h,img):
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

    #print("read canvas:")
    #print(can_w,can_h)
    #print("read images")
    #print(raw_w,raw_h)
    #print("the ratio")
    #print(ratio_w,ratio_h)
    #print("result:")
    #print(x,y,w,h)
    for i in range(h):
        for j in range(w):
            img[i+y][x+j] =[0,0,0]
    #img=img.rectangle((60,90,100,120), fill = (0,0,0))
    return img


tempt_seq=""  
tempt_seq_clear ="" 
tempt_caption_list = [] 
tempt_caption_words=[] 
tempt_total_words=[] 
tempt_catg_num = 0

from datetime import timedelta

app = Flask(__name__)
 
 
# 设置图片保存文件夹
UPLOAD_FOLDER = 'photo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
 
app.send_file_max_age_default = timedelta(seconds=0.001)

 
# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS
 
# 设置静态文件缓存过期时间
#app.send_file_max_age_default = timedelta(seconds=10)
 
def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream
    
@app.route('/home/', methods=['POST', "GET"])
def home():
    global tempt_seq , tempt_seq_clear, tempt_caption_list, tempt_caption_words, tempt_total_words, tempt_catg_num
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        global file_name 
        file = request.files['file']

        Beam_size = int(request.form['BEAM'])

        if file and allowed_file(file.filename):
            print(file.filename)
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            img_path=os.path.join(basepath,app.config['UPLOAD_FOLDER'], file_name)
            
            ## New added by Dongzi:
            #image_vector = get_vector(img_path)
            test_index = file_name.split('.')[0][4:]
            test_index = int(test_index)
            image_vector = test_vec[test_index-1]
            #print(test_index)
            #print(image_vector)
            image_label = get_label(image_vector)
            image_list = get_top_images(image_label, image_vector, k=5)
            caption_list = add_caption(image_list)
            #print("The label of this image is: %d" % (image_label))
            #print("The image_list is:", image_list)
            #print(caption_list)
            caption_words, total_words, catg_num, tag_num = word_static(image_label)
            #print(caption_words)

            for i in range(len(image_list)):
                same_class_img_from_path = './pretrained/Flickr_Data/Images/' + str(image_list[i]) + '.jpg'
                same_class_img_save_path = os.path.join(basepath, 'static/images',str(i)+'.jpg')
                same_class_img = cv.imread(same_class_img_from_path)
                cv.imwrite(same_class_img_save_path, same_class_img)
            ## End by Dongzi



            # 保存图片
            file.save(img_path)
            #figfile = io.BytesIO(open(img_path, 'rb').read())
            #img = return_img_stream(img_path)
            static_path = os.path.join(basepath, 'static/images','test.jpg')
            print(static_path)
            if(os.path.exists(static_path)):
                os.remove(static_path)
            img = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            cv.imwrite( static_path,img)

            seq, seq_clear= test_photo(img_path, beam_size = Beam_size)
            #seq = test_photo(img_path, beam_size = Beam_size)
            print(seq)

            # save to global
            tempt_seq, tempt_seq_clear, tempt_caption_list  =  seq, seq_clear, caption_list
            tempt_caption_words, tempt_total_words, tempt_catg_num = caption_words, total_words, catg_num
            return render_template('main.html', val1=time.time(), text =seq, text_clear=seq_clear, length = len(seq), generated_seq = seq_clear, cap_list = caption_list, cap_words = caption_words, words_num = total_words, words_cat = catg_num, tag_num = tag_num)
        else:
            #flash("wrong format, please uplead .jpg file", "warning")
            return "wrong format, please uplead .jpg/.png/.jpeg file"
    elif request.method == 'GET':
            [canvas_width, canvas_height]=[request.args.get('canvas_w'),request.args.get('canvas_h')]
            [x,y,width,height]=[request.args.get('x'),request.args.get('y'),request.args.get('width'),request.args.get('height')]
            print(canvas_width, canvas_height,x,y,width,height)
            if canvas_width:
                img = cv.imread("./static/images/test.jpg")
                new_img = generate_new_image(canvas_width, canvas_height,x,y,width,height,img)
                  # get new caption
                base_path = os.getcwd()
                new_img_path = os.path.join(base_path, 'static/images','generated_test.jpg')
                if(os.path.exists(new_img_path)):
                        os.remove(new_img_path)
                cv.imwrite(new_img_path,new_img)
                new_seq= test_photo_easy(new_img_path)
                print(new_seq)
                
                # save new string to file
                fn = base_path+"/static/text/new_caption.txt"
                fh = open(fn,'w')
                fh.write(new_seq)
                fh.close()
                return render_template('main.html',val1=time.time(), text =tempt_seq, text_clear=tempt_seq_clear, length = len(tempt_seq), cap_list = tempt_caption_list, \
                    cap_words = tempt_caption_words, words_num = tempt_total_words, words_cat = tempt_catg_num, generated_seq = new_seq)
                #return new_seq

    return render_template("home.html")

 # 查看图片
@app.route("/photo/<imageId>.jpg")
def get_frame(imageId):
    # 图片上传保存的路径
    #with open(r'C:/Users/60587/Desktop/CapVis/static/images/test_.jpg'.format(imageId), 'rb') as f:
    with open(r'/Users/qdz/Desktop/NYU_courses/Semester_2/9223-I_Connection_ML/project/CapVis-master/static/images/'+imageId+'.jpg', 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp       
# 查看图片
@app.route("/photo/caption")
def get_caption():
    # 图片上传保存的路径
    #with open(r'C:/Users/60587/Desktop/CapVis/static/images/test_.jpg'.format(imageId), 'rb') as f:
    with open(r'/Users/qdz/Desktop/NYU_courses/Semester_2/9223-I_Connection_ML/project/CapVis-master/static/text/new_caption.txt', 'rb') as f:
        txt = f.read()
        resp = Response(txt, mimetype="text/plain")
        return resp       
# 查看图片
@app.route("/photo/csv")
def get_csv():

    with open(r'/Users/qdz/Desktop/NYU_courses/Semester_2/9223-I_Connection_ML/project/CapVis-master/static/text/pic_tag_frequency.csv', 'rb') as f:
        csv = f.read()
        #print (json)
        #return json
        resp = Response(csv, mimetype="application/csv")
        return resp  

@app.route("/photo/json_f")
def get_freq():
    with open(r'/Users/qdz/Desktop/NYU_courses/Semester_2/9223-I_Connection_ML/project/CapVis-master/static/text/pic_frequency.json', 'rb') as f:
        csv = f.read()
        #print (json)
        #return json
        resp = Response(csv, mimetype="application/json")
        return resp 

@app.route("/photo/jsontag")
def get_tag():
    with open(r'/Users/qdz/Desktop/NYU_courses/Semester_2/9223-I_Connection_ML/project/CapVis-master/static/text/pic_tag.json', 'rb') as f:
        csv = f.read()
        #print (json)
        #return json
        resp = Response(csv, mimetype="application/json")
        return resp  
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


