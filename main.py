#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphic.convert import *
import os

image = os.path.abspath('_LST8799.jpg')
blur_image(image)
resize_image(image, THUMBS_IMAGE)