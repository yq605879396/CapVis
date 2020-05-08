from flask import Flask, Response, request, render_template, url_for, make_response
from caption import test_photo, test_photo_easy
from utils import *
from werkzeug.utils import secure_filename
from datetime import timedelta

import os, io, time, json

import cv2 as cv

import matplotlib.pyplot as plt


app = Flask(__name__)

# set the last time of static files's cache 
app.send_file_max_age_default = timedelta(seconds=0.001)


# set the directory to save uploaded image
UPLOAD_FOLDER = 'uploaded_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# set the limitation of uploaded image's format
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
  
# check if uploaded file have suitable format
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

# the main website to serve 
@app.route('/home/', methods=['POST', "GET"])
def home():
    global tempt_seq , tempt_seq_clear, tempt_caption_list, tempt_caption_words, tempt_total_words, tempt_catg_num
    if request.method == 'POST':

        global file_name 
        
        file = request.files['file']
        Beam_size = int(request.form['BEAM'])

        if file and allowed_file(file.filename):

            # notice secure_filename method will remove chinese in the name
            file_name = secure_filename(file.filename)
            img_path=os.path.join(current_path,app.config['UPLOAD_FOLDER'], file_name)
            
            # retrieve information of correspondng cluster
            test_index = file_name.split('.')[0][4:]
            test_index = int(test_index)
            image_vector = test_vec[test_index-1]
            image_label = get_label(image_vector)
            image_list = get_top_images(image_label, image_vector, k=5)
            caption_list = add_caption(image_list)
            caption_words, total_words, catg_num, tag_num = word_static(image_label)

            for i in range(len(image_list)):
                same_class_img_from_path = './pretrained/Flickr_Data/Images/' + str(image_list[i]) + '.jpg'
                same_class_img_save_path = os.path.join(current_path, 'static/show_as_website/images',str(i)+'.jpg')
                same_class_img = cv.imread(same_class_img_from_path)
                cv.imwrite(same_class_img_save_path, same_class_img)


            # save uploaded image
            file.save(img_path)
            static_path = os.path.join(current_path, 'static/show_as_website/images','test.jpg')
            if(os.path.exists(static_path)):
                os.remove(static_path)
            img = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            cv.imwrite( static_path,img)
            cv.imwrite( current_path + 'static/show_as_website/images/generated_test.jpg',img)

            seq, seq_clear = test_photo(img_path, beam_size = Beam_size)

            # save to global
            tempt_seq, tempt_seq_clear, tempt_caption_list  =  seq, seq_clear, caption_list
            tempt_caption_words, tempt_total_words, tempt_catg_num = caption_words, total_words, catg_num

            return render_template('main.html', val1 = time.time(), text = seq, text_clear = seq_clear, length = len(seq), generated_seq = seq_clear, cap_list = caption_list, cap_words = caption_words, words_num = total_words, words_cat = catg_num, tag_num = tag_num)
        else:
            return "wrong format, please uplead .jpg/.png/.jpeg file"

    elif request.method == 'GET':

            # retrieve information from the html
            [canvas_width, canvas_height] = [request.args.get('canvas_w'),request.args.get('canvas_h')]
            [x,y,width,height] = [request.args.get('x'),request.args.get('y'),request.args.get('width'),request.args.get('height')]

            if canvas_width:

                # generate new image and save it
                img = cv.imread("./static/show_as_website/images/test.jpg")
                new_img = generate_new_image(canvas_width, canvas_height,x,y,width,height,img)
                new_img_path = os.path.join(current_path, 'static/show_as_website/images','generated_test.jpg')
                if(os.path.exists(new_img_path)):
                        os.remove(new_img_path)
                cv.imwrite(new_img_path,new_img)

                # generate new caption and write it into file
                new_seq = test_photo_easy(new_img_path)
                fh = open(current_path+"/static/show_as_website/text/new_caption.txt",'w')
                fh.write(new_seq)
                fh.close()

                return render_template('main.html',val1=time.time(), text =tempt_seq, text_clear=tempt_seq_clear, length = len(tempt_seq), cap_list = tempt_caption_list, \
                    cap_words = tempt_caption_words, words_num = tempt_total_words, words_cat = tempt_catg_num, generated_seq = new_seq)

    return render_template("home.html")

 # visulize the photo in ./static/images directory
 # contains test.jpg, generated_test
 #      5 most similar pictures with test.jpg, named 1/2/3/4/5.jpg
@app.route("/vis/<imageId>.jpg")
def get_frame(imageId):
    #with open(r'C:/Users/60587/Desktop/CapVis/static/images/test_.jpg'.format(imageId), 'rb') as f:
    with open(current_path +'/static/show_as_website/images/' + imageId + '.jpg', 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp       

# after user mask a image with the interface provided in "main.html", we generate a new caption
# used by "show_new_caption('ID')" in main.html's js functions
@app.route("/vis/caption")
def get_caption():
    #with open(r'C:/Users/60587/Desktop/CapVis/static/images/test_.jpg'.format(imageId), 'rb') as f:
    with open(current_path +'/static/show_as_website/text/new_caption.txt', 'rb') as f:
        txt = f.read()
        resp = Response(txt, mimetype = "text/plain")
        return resp       

# select the cluster that upload imag belongs to, show this cluster's word frequency 
# used by "pie_char1" in main.html
@app.route("/vis/json_word_frequency")
def get_freq():
    with open(current_path +'/static/show_as_website/text/pic_frequency.json', 'rb') as f:
        csv = f.read()
        resp = Response(csv, mimetype = "application/json")
        return resp 

# select the cluster that upload imag belongs to, show this cluster's part-of-speech(tag) distribution
# used by "pie_chart2" in main.html 
@app.route("/vis/json_word_tag")
def get_tag():
    with open(current_path + '/static/show_as_website/text/pic_tag.json', 'rb') as f:
        csv = f.read()
        #print (json)
        #return json
        resp = Response(csv, mimetype = "application/json")
        return resp  
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


