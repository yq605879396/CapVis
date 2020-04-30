from flask import Flask, Response, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
from caption import test_photo
from flask import make_response
import cv2 as cv
import io
import time

from datetime import timedelta

app = Flask(__name__)
 
 
# 设置图片保存文件夹
UPLOAD_FOLDER = 'photo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
 
app.send_file_max_age_default = timedelta(seconds=1)

 
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
    return render_template("home.html")

# 上传图片页面nc=upload_image, methods=["POST"])
@app.route('/upload/', methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        global file_name 
        file = request.files['file']
        if file and allowed_file(file.filename):
            print(file.filename)
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            img_path=os.path.join(basepath,app.config['UPLOAD_FOLDER'], file_name)
            
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

            seq= test_photo(img_path)
            print(seq)
            return render_template('result.html', val1=time.time(), text =seq)
        else:
            #flash("wrong format, please uplead .jpg file", "warning")
            return "wrong format, please uplead .jpg/.png/.jpeg file"
    return render_template('upload_image.html')


# 展示分析页面
#app.add_url_rule(rule="/predict/", endpoint="predict", view_func=caption_predict)
@app.route("/result", methods=['show', "feedback","good","bad"])
def caption_predict():
    global file_name
    img= app.config['UPLOAD_FOLDER']+'/'+file_name
    #使用Opencv转换一下图片格式和名称

    img, seq, alphas, rev_word_map =  test_photo(image)
    return render_template('result.html')
    #show(img, seq, alphas, rev_word_map,smooth=True)

def show(image_path, seq, alphas, rev_word_map,smooth=True):
    image = Image.open(image_path)
    image = image.resize([14 * 24, 14 * 24], Image.LANCZOS)

    words = [rev_word_map[ind] for ind in seq]

    for t in range(len(words)):
        if t > 50:
            break
        plt.subplot(np.ceil(len(words) / 5.), 5, t + 1)

        plt.text(0, 1, '%s' % (words[t]), color='black', backgroundcolor='white', fontsize=12)
        plt.imshow(image)
        current_alpha = alphas[t, :]
        if smooth:
            alpha = skimage.transform.pyramid_expand(current_alpha.numpy(), upscale=24, sigma=8)
        else:
            alpha = skimage.transform.resize(current_alpha.numpy(), [14 * 24, 14 * 24])
        if t == 0:
            plt.imshow(alpha, alpha=0)
        else:
            plt.imshow(alpha, alpha=0.8)
        plt.set_cmap(cm.Greys_r)
        plt.axis('off')
    plt.show()
 
 
# 查看图片
@app.route("/photo/<imageId>.jpg")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'C:/Users/Administration/Desktop/photo_ceshi/photo/{}.jpg'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


