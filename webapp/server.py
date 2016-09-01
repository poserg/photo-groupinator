#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path as sys_path
sys_path.append('../')
import os
#from werkzeug.exceptions import BadRequest
from flask import Flask, request, jsonify, abort, Response, \
     send_from_directory
from flask_restful import Resource, Api, fields, marshal_with
from flask.ext.cors import cross_origin
from dao.db import *
from functools import wraps

import logging
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

app = Flask(__name__, static_folder = '../images/static', static_url_path='/../client')
app.secret_key = os.urandom(24)
app.debug = True

api = Api(app)

CONTENT_TYPE = {'Content-Type': 'application/json; charset=utf-8'}
BAD_REQUEST = "BAD_REQUEST", 400

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
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../client', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../client', path)

photo_resource_fields = {
    'id': fields.Integer,
    'name' : fields.String,
    'create_date' : fields.String
}

class Photo(Resource):
    @marshal_with(photo_resource_fields)
    def get(self, id):
        #abort_if_photo_doesnt_exist(id)
        return db.get_image_by_id(id)

    def put(self, id):
        pass

api.add_resource(Photo, '/photos/<int:id>')

class PhotoList(Resource):
    @marshal_with(photo_resource_fields)
    def get(self):
        return db.get_images()

api.add_resource(PhotoList, '/photos')

group_resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'operations' : fields.List(fields.Integer)
}

class Group(Resource):
    @marshal_with(group_resource_fields)
    def get(self, id):
        group = db.get_group_by_id(id)
        if type(group) is Group:
            return group
        else:
            return abort(404)

    def put(self, id):
        logging.info('Create group')
        return make_group(request)
        

api.add_resource(Group, '/groups/<int:id>')

class GroupList(Resource):
    @marshal_with(photo_resource_fields)
    def get(self):
        return db.get_groups()

api.add_resource(GroupList, '/groups')
    
def make_group(request):
    logging.info('Make group')
    data = request.json
    if data:
        name = "Unnamed" if not data.has_key('name') else data['name']
        result = db.create_group(name)
        if result > 0:
            return "CREATED", 201
    else:
        return BAD_REQUEST

rule_resource_fields = {
    'id': fields.Integer,
    'name' : fields.String,
    'type' : fields.String(attribute=lambda x: 'null' if x is None \
                           else x.operation_type.name)
}

class RuleList(Resource):
    @marshal_with(rule_resource_fields)
    def get(self):
        return db.get_rules()

api.add_resource(RuleList, '/rules')

class Rule(Resource):
    @marshal_with(rule_resource_fields)
    def get(self, id):
        return db.get_rule_by_id(id)

    def put(self, id):
        return make_rule(request)

api.add_resource(Rule, '/rules/<int:id>')

def make_rule(request):
    logging.info('Make rule')
    data = request.json
    if data:
        name = 'Unnamed' if not data.has_key('name') else data['name']
        result = db.create_rule(name)
        if result > 0:
            return 'CREATED', 201
    else:
        return BAD_REQUEST
    
if __name__ == '__main__':
    from flask.ext.cors import CORS
    cors = CORS(app)
    app.run(host='0.0.0.0', port=8080)
