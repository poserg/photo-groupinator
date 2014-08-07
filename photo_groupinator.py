#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os import path, listdir
from graphic import convert

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
	for i in files:
		ext = path.splitext(p[0] + '/' + i)[1]
		if ext != ".png" and ext != ".JPG":
			files.remove(i)
	print files