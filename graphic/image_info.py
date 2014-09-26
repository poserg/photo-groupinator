# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS

def get_info(path):
	print (get_field(path, 'DateTime'))

def get_create_date(path):
	return get_field(path, 'DateTime')


def get_field (path,field) :
	exif = get_exif(path)
	if (exif is not None):
		for (k,v) in exif.iteritems():
			if TAGS.get(k) == field:
				return v

def get_size (path):
    exif = Image.open(path)
    return exif.size

def get_exif(path):
    return Image.open(path)._getexif()

def get_fields(path):
    exif = get_exif(path)
    for (k, v) in exif.iteritems():
        print '%s = %s' % (TAGS.get(k), v)

def get_orientation(path):
    orientation = get_field(path, 'Orientation')
    if orientation is not None:
        return int(orientation) > 4
    else:
        return False
