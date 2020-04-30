# CapVis
A Visulization Of Image Caption

## notice：
we didn't put the pretrained model in this repository, since its so huge
Please download from "https://drive.google.com/open?id=1V2PQ7uGgEKv2Wp91p1CAoUBVivcvCLqg"

## Command
# visualization
python App.py
Then open "http://127.0.0.1:5000/home/" in Chrome

# test a photo and plot the image
python caption.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='pretrained/test7.jpg'

# print the caption out
python get_cap.py --model='pretrained/BEST_checkpoint_flickr30k_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='pretrained/WORDMAP_flickr30k_5_cap_per_img_5_min_word_freq.json' --beam_size=5 --img='pretrained/test4.jpg'