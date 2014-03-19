# -*- coding: utf-8 -*-

from PIL import Image

#convert $ftmp -gamma 0.454545 -geometry "$maxfull[0]x$maxfull[1]>" -print %w\n%h -gamma 2.2 +profile !icc* -quality $imgq "$out/$fimg" 

# Generate main image
# convert -quality 90 -resize 1600x1067 IMG_1203.JPG my_out.jpg

# Thumbs
# convert -quality 90 -resize 168x112 IMG_1203.JPG my_out.jpg

# Blur
# convert my_out.jpg -virtual-pixel Mirror -gaussian-blur 0x8 -scale 252x336 -quality 90 my_out_blur.jpg
