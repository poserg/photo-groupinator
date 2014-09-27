# -*- coding: utf-8 -*-

from sys import path as sys_path
sys_path.append('../')

from subprocess import call
from util.fs_util import get_dir, get_dist_path, copy_file

from image_info import get_info, get_orientation

import logging
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

MAIN_IMAGE = ("main", "1600", "1067")
THUMBS_IMAGE = ("static/thumbs", "168", "112")
BLUR_IMAGE = ("static/blur")

def resize_image(image_path, dist_path, t):
    """Generate main image
    convert -quality 90 -resize 1600x1067 IMG_1203.JPG my_out.jpg
    
    Thumbs
    convert -quality 90 -resize 168x112 IMG_1203.JPG my_out.jpg"""


    dist_path = get_dist_path(dist_path, t[0], image_path)
    get_info(image_path)

    width = t[1]
    height = t[2]
    if get_orientation(image_path):
        width = t[1]
        height = str(int(t[1])/2*3)
        
    params = [
        "-geometry",
        width + "x" + height,
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
    logging.debug("Start convert image")
    params =["convert",
             "-quality",
             "90",
             "-auto-orient"
             ]
    params += additional_params
    logging.debug (params)
    retcode = call(params)
    
    if retcode != 0:
        logging.error("Error with coverting file: " + additional_params[-2])
    logging.debug("Image converted")

def copy_image(image_path, dist_path):
  copy_file(image_path, get_dir(dist_path, "orig"))

#def find_duplicate(path):
    
