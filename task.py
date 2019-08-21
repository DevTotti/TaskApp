from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongotask'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mongotask"

mongo = PyMongo(app)

CORS(app)

@app.route("/api/tasks", methods=['GET'])
def get_all_tasks():
	task=mongo.db.tasks

	result = []

	for field in task.find():
		result.append({'_id':str(field['_id']), 'title':str(field['title']), 'description':str(field['description'])})

	return jsonify(result)


@app.route('/api/tasks', methods=['POST'])
def add_task():
	tasks = mongo.db.tasks
	title = request.get_json()['title']
	description = request.get_json()['description']

	task_id = tasks.insert({'title':title})
	new_task = tasks.find_one({'_id': task_id})

	result = {'title':new_task['title']}

	return jsonify({'result':result})


@app.route('api/task/<id>', methods=['PUT'])
def update_task(id):
	task = mongo.db.tasks
	title = request.get_json()['title']
	description = request.get_json()['description']

	tasks.find_one_and_update({
		'_id':ObjectId(id)
		}, {"$set":{"title": title},{"description": description}

		}, upsert=False)

	new_task = task.find_one({'_id': ObjectId})

	result = {'title':new_task['title']}

	return jsonify({'result':result})



@app.route('api/task/<id>', methods=['DELETE'])
def delete_task(id):
	tasks = mongo.db.tasks

	response = tasks.delete_one({'_id':ObjectId(id)})

	if response.deleted_count == 1:
		result = {'message':'record deleted'}

	else:
		result = {'message': 'no record found'}

	return jsonify({'result':result})



if __name__ == '__main__':
	app.run(host="localhost", port=5001, debug=True)