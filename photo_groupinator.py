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

if __name__ == '__main__':
	app.run()
