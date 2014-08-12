#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path, listdir
from graphic.convert import *
from core import *

def print_help():
	print ("Help info")

p = []
if len(argv) == 1:
	print_help()
else:
	for i in argv[1:]:
		if i == "-fd":
			print ("Find duplicate is on")
		else:
			p.append(path.abspath(i))
			if (len(p) > 2):
				print_help()

	files = listdir(p[0])
	print files
	image_files = filter(lambda x: path.splitext(p[0] + '/' + x)[1].upper() in [".JPG", ".JPEG", ".PNG"],files)

	# map(lambda x: blur_image(x, p[1]), image_files)
	# map(lambda x: resize_image(x, p[1], THUMBS_IMAGE), image_files)
	# map(lambda x: resize_image(x, p[1], MAIN_IMAGE), image_files)
	# map(lambda x: copy_image(x, p[1]), image_files)

	db_util = DBUtil(p[1])

	for image in image_files:
		blur_image(image, p[1])
		resize_image(image, p[1], THUMBS_IMAGE)
		resize_image(image, p[1], MAIN_IMAGE)
		copy_image(image, p[1])

		name = path.basename(image)
		db_util.insert_image(name, image)

