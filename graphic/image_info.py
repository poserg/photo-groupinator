# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS

def get_info(path):
	exif = Image.open(path)._getexif()
	print (get_field(exif, 'DateTime'))

def get_create_date(path):
	exif = Image.open(path)._getexif()
	return get_field(exif, 'DateTime')


def get_field (exif,field) :
	if (exif is not None):
		for (k,v) in exif.iteritems():
			if TAGS.get(k) == field:
				return v
