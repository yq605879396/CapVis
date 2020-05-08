# CapVis
A Visulization Of Image Caption
(in development ....)


# notice：
we didn't put the pretrained files in this repository, since they are so huge
Please download from "https://drive.google.com/open?id=1V2PQ7uGgEKv2Wp91p1CAoUBVivcvCLqg"

little bugs：
1. Please remember to input the beam size
2. After mask pictures, it may take a while to generate new caption, if the caption is the old one, please click "update" again.

# How to use it
### requirments: python3,  nltk, numpy, pytorch, flask
# there are three ways to use it 
## visualization (main part)
python App.py
Then open "http://127.0.0.1:5000/home/" in Chrome
please upload an image from image test or you can whatever image but generate a vector for it before upload it, for details see:
?????

## test a photo and plot the image
python caption.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='pretrained/test7.jpg'

## simply print the caption out in console
python get_cap.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='pretrained/test4.jpg'

# some related resource 
## obsevable used
### static data already upload
https://observablehq.com/@yq605879396/artsed-bubble
https://observablehq.com/@yq605879396/zoomable-sunburst/2

### fetching data while the server is running
https://observablehq.com/@yq605879396/pie-chart
https://observablehq.com/@yq605879396/pie-chart/2
https://observablehq.com/@yq605879396/mona-lisa-histogram/2


# referring
### computation module:
https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning 
This is an outstanding implementation of "show, attend and tell" in pytorch version

### html template
https://codyhouse.co/gem/vertical-fixed-navigation-2/ 
we rewrite our website base on this frame