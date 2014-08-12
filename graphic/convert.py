# -*- coding: utf-8 -*-

# from PIL import Image
from subprocess import call
import os

MAIN_IMAGE = ("main", "1600x1067")
THUMBS_IMAGE = ("thumbs", "168x112")
BLUR_IMAGE = ("blur")

def mkdir(path):
    #os.makedirs(path, exist_ok = True)
    try:
      os.makedirs(path)
    except OSError, e:
      #print "Directory is exists"
      pass
    return path
    # d = os.path.dirname(path)
    # if not os.path.exists(d):
    #     os.makedirs(d)
        
    # return d

def get_dir(path, file_name):
  if len(path) > 0 and path[-1] == "/":
    return mkdir(path + file_name)
  else:
    return mkdir(path + "/" + file_name)


def resize_image(image_path, dist_path, t):
    """Generate main image
    convert -quality 90 -resize 1600x1067 IMG_1203.JPG my_out.jpg
    
    Thumbs
    convert -quality 90 -resize 168x112 IMG_1203.JPG my_out.jpg"""


    dist_path = get_dir(dist_path, t[0])
    params = [
        "-resize",
        t[1],
        image_path,
        dist_path + "/" + os.path.basename(image_path)
        ]
    convert_image(params)
    
def blur_image(image_path, dist_path):
    """Blur
    convert my_out.jpg -virtual-pixel Mirror -gaussian-blur 0x8 -scale 252x336 -quality 90 my_out_blur.jpg"""
    dist_path = get_dir(dist_path, "blur")
    params = ["-virtual-pixel",
              "Mirror",
              "-gaussian-blur",
              "0x8",
              "-scale",
              "252x336",
              image_path,
              dist_path + "/" + os.path.basename(image_path)]
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

#def find_duplicate(path):
    
