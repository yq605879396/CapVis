# CapVis
## outline
* Name: Visualization System for Image Captioning (Course Project)
* Contributors: [Qi Yin](qy652@nyu.edu), [Dongzi Qu](dq394@nyu.edu)
* Instructors: [Claudio Silva](csilva@nyu.edu), [Jorge Piazentin Ono](jpo286@nyu.edu), [Yeuk Yin Chan](gromit.chan@nyu.edu)
* Institute: NYU Tandon School of Engineering (Dept: Computer Science)

# Notice：
Little bugs：
1. Please remember to input the beam size
2. After mask pictures, it may take a while to generate new caption, if the caption is the old one, please click "update" again.


# How to use it
### Requirements: 

python3,  nltk, numpy, pytorch, flask

### Files need to Download：

After clone this project, please download the pretrained file and put in "CapVis/pretrained" respository:

CapVis/pretrained ____  Flickr_Data<br>
&emsp;  &emsp;	&emsp; &emsp; &emsp; &emsp; &emsp; |__  BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar<br>
&emsp;	&emsp;	&emsp; &emsp; &emsp; &emsp; &emsp; |__  WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json<br>
&emsp;	&emsp;	&emsp; &emsp; &emsp; &emsp; &emsp; |__  All_vectors<br>
&emsp;	&emsp;	&emsp; &emsp; &emsp; &emsp; &emsp; |__  center_100<br>
&emsp;	&emsp;	&emsp; &emsp; &emsp; &emsp; &emsp; |__  ...<br><br>
File link:

1. Pretrained computation model:<br>
Trained with flickr30k: "https://drive.google.com/open?id=1V2PQ7uGgEKv2Wp91p1CAoUBVivcvCLqg"    (This is trained by us)<br>
Trained with COCO: "https://drive.google.com/drive/folders/189VY65I_n4RTpQnmLGj7IzVnOF6dmePC"   (This is trained by sgrvinod)<br>

&#8194;&#8194;&#8194;  ps: The code now is using flickr30k model.  If you want to use COCO model, remember to change the path in "caption.py".

2. Other files
"https://drive.google.com/file/d/1YmbJQXCAv08mNnpmtKHjWV4s2rQ1C3QL/view?usp=sharing"



### There are three ways to use it Website

### 1. Visualization On Website (main part)
python App.py
Then open "http://127.0.0.1:5000/home/" in Chrome
please upload an image from image test or you can whatever image but generate a vector for it before upload it, for details see:
?????

### 2. Test a photo and plot the image
python caption.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='image_for_test/test7.jpg'



### 3. Simply print the caption out in console
python get_cap.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='image_for_test/test4.jpg'

# Related resource 
### Observable D3 used：

Static data already upload：

https://observablehq.com/@yq605879396/artsed-bubble
https://observablehq.com/@yq605879396/zoomable-sunburst/2

Fetching data while the server is running：

https://observablehq.com/@yq605879396/pie-chart
https://observablehq.com/@yq605879396/pie-chart/2
https://observablehq.com/@yq605879396/mona-lisa-histogram/2


# Referring
### Computation Module:
https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning 
This is an outstanding implementation of "show, attend and tell" in pytorch version

### HTML template
https://codyhouse.co/gem/vertical-fixed-navigation-2/ 
we rewrite our website base on this frame
