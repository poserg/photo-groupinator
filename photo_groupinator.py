#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
        return 'Photo Groupinator'

@app.route('/photo/<int:photo_id>', methods=['GET', 'PUT'])
def photo(photo_id):
        if request.method == 'GET':
                return 'Photo %d' % photo_id
        elif request.method == 'PUT':
                return 'Change photo %d' % photo_id

@app.route('/group/<int:group_id>', methods=['GET', 'PUT', 'DELETE'])
def group(group_id):
        pass

@app.route('/group', methods=['POST'])
def create_group():
        pass

if __name__ == '__main__':
        app.run()
