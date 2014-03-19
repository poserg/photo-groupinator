#!/usr/bin/env python

from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/photo/<int:photo_id>', methods=['GET', 'PUT'])
def photo(photo_id):
	if request.method == 'GET':
		return 'Photo %d' % photo_id
	elif request.method == 'PUT':
		return 'Change photo %d' % photo_id

@app.route('/group/<int:group_id>', methods=['GET', 'PUT'])
def group(group_id):
	pass

if __name__ == '__main__':
	app.run()
