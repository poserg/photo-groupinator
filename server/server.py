#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path as sys_path
sys_path.append('../')
from flask import Flask, request, jsonify, abort
from dao.db import *

app = Flask(__name__)
app.debug = True

db = DBUtil('../images')

@app.route('/')
def main():
    return 'Photo Groupinator'

@app.route('/photo/<int:photo_id>', methods=['GET', 'PUT'])
def get_photo(photo_id):
    if request.method == 'GET':
    	image = db.get_image_by_id(photo_id)
    	if type(image) is Image:
        	#return 'Photo %s' % image.name
        	return jsonify(id = image.id, name = image.name, create_date = image.create_date)
        else:
        	abort(404)
    elif request.method == 'PUT':
        return 'Change photo %d' % photo_id

@app.route('/photo', methods=['GET'])
def get_photos():
  	images = db.get_images()
	return jsonify(photos=[i.serialize for i in images])

@app.route('/group/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
def group(group_id):
    pass

@app.route('/group', methods=['POST'])
def create_group():
    pass

if __name__ == '__main__':
    app.run()
