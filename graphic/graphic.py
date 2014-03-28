# -*- coding: utf-8 -*-

from PIL import Image
from subprocess import call

MAIN_IMAGE = ("main", "1600x1067")
THUMBS_IMAGE = ("thumbs", "168x112")
BLUR_IMAGE = ("blur")

def get_dir(path):
    os.makedirs(path, exist_ok = True)
    # d = os.path.dirname(path)
    # if not os.path.exists(d):
    #     os.makedirs(d)
        
    # return d


def resize_image(image_path, t):
    """Generate main image
    convert -quality 90 -resize 1600x1067 IMG_1203.JPG my_out.jpg
    
    Thumbs
    convert -quality 90 -resize 168x112 IMG_1203.JPG my_out.jpg"""
    get_dir(t[0])
    params = [
        "-resize",
        t[1],
        image_path,
        t[0] + "/" + os.path.basename(image_path)
        ]
    convert_image(params)
    
def blur_image(image_path):
    """Blur
    convert my_out.jpg -virtual-pixel Mirror -gaussian-blur 0x8 -scale 252x336 -quality 90 my_out_blur.jpg"""
    get_dir("blur")
    params = ["-virtual-pixel",
              "Mirror",
              "-gaussian-blur",
              "0x8",
              "-scale"
              "252x336"]
    convert_image(params)
    
def convert_image(additional_params):
    params =["convert",
             "-quality",
             "90"
             ]
    params += additional_params
    
    retcode = call(params)
    
    if recode != 0:
        print "Error with coverting file: " + additional_params[-2]
    

def find_duplicate(path):
    
