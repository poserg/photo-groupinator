# -*- coding: utf-8 -*-

from sys import path as sys_path
sys_path.append('../')

# from PIL import Image
from subprocess import call

from util.fs_util import get_dir, get_dist_path, copy_file

MAIN_IMAGE = ("main", "1600x1067")
THUMBS_IMAGE = ("thumbs", "168x112")
BLUR_IMAGE = ("blur")

def resize_image(image_path, dist_path, t):
    """Generate main image
    convert -quality 90 -resize 1600x1067 IMG_1203.JPG my_out.jpg
    
    Thumbs
    convert -quality 90 -resize 168x112 IMG_1203.JPG my_out.jpg"""


    dist_path = get_dist_path(dist_path, t[0], image_path)
    params = [
        "-resize",
        t[1],
        image_path,
        dist_path
        ]
    convert_image(params)
    
def blur_image(image_path, dist_path):
    """Blur
    convert my_out.jpg -virtual-pixel Mirror -gaussian-blur 0x8 -scale 252x336 -quality 90 my_out_blur.jpg"""
    dist_path = get_dist_path(dist_path, "blur", image_path)
    params = ["-virtual-pixel",
              "Mirror",
              "-gaussian-blur",
              "0x8",
              "-scale",
              "252x336",
              image_path,
              dist_path]
    convert_image(params)
    
def convert_image(additional_params):
    # print ("Start convert image")
    params =["convert",
             "-quality",
             "90"
             ]
    params += additional_params
    print (params)
    retcode = call(params)
    
    if retcode != 0:
        print "Error with coverting file: " + additional_params[-2]
    # print ("Image converted")

def copy_image(image_path, dist_path):
  copy_file(image_path, get_dir(dist_path, "orig"))

#def find_duplicate(path):
    
