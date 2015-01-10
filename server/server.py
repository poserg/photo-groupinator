#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path as sys_path
sys_path.append('../')
import os
from flask import Flask, request, jsonify, abort, Response
from flask.ext.cors import cross_origin
from dao.db import *
from functools import wraps

import logging
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

app = Flask(__name__, static_folder = '../images/static')
app.secret_key = os.urandom(24)
app.debug = True

db = DBUtil('../images')

from datetime import timedelta
from functools import update_wrapper
from flask import make_response, request, current_app
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return decorated_function

@app.route('/')
#@crossdomain(origin='*')
def main():
    return 'Photo Groupinator', 200

@app.route('/photo/<int:photo_id>', methods=['GET', 'PUT'])
#@crossdomain(origin='*')
@returns_json
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
#@cross_origin(supports_credentials = True)
#@crossdomain(origin='*')
def get_photos():
  	images = db.get_images()
	return jsonify(photos=[i.serialize for i in images]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/group/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
def group(group_id):
    if request.method == 'GET':
        group = db.get_group_by_id(group_id)
        if type(group) is Group:
            return jsonify(id = group.id, name = group.name)
        else:
            return abort(404)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

@app.route('/group', methods=['GET'])
def get_groups():
    groups = db.get_groups()
    return jsonify(groups=[i.serialize for i in groups])
    
@app.route('/group', methods=['POST'])
def create_group():
    pass

if __name__ == '__main__':
    from flask.ext.cors import CORS
    cors = CORS(app)
    app.run(host='0.0.0.0', port=8080)
