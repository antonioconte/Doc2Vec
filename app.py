import json
from config import *
from flask_cors import CORS
from flask import Flask,request
from doc2vec import Doc2Vec_model
from preprocess.utils import remove_tag
from utils import metrics

app = Flask(__name__)
model = None

CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/connect/', methods=['GET'])
def load_model():
	global model
	msg = {}
	if model == None:
		model = Doc2Vec_model(type="S")
		path_model = model.load()
		msg['data'] =  path_model
	else:
		msg['data'] = "Model already loded"	
	response = app.response_class(
		response=json.dumps(msg, indent=4),
		status=200,
		mimetype='application/json'
	)
	return response

@app.route('/query/', methods=['POST'])
def query():
	# txt da pulire dei tag dell'html
	txt = request.json['data']
	response = sections(txt)
	return response

def sections(txt):
	txt = remove_tag(txt) # txt da pulire dei tag dell'html
	(time,res) = model.predict(txt)
	(_, res) = metrics.compute(txt, res)
	msg = {'data': res,'query':txt,'time': time}
	response = app.response_class(
			   	response=json.dumps(msg, indent=4),
			   	status=200,
			   	mimetype='application/json'
	)
	return response


@app.route('/train/', methods=['POST'])
def train():
	# txt da pulire dei tag dell'html
	data = request.json
	model_to_train = Doc2Vec_model(type=data['type'], path=data['path'])
	msg = {'path': data['path'], 'type': data['type']}
	print("Start training [{}] with directory: {}".format(msg['type'],msg['path']))
	try:
		m = model_to_train.train()
		status = 200
		msg['res'] = "Num of documents learned: {}".format(len(m.docvecs))
	except:
		status = 505
		msg['res'] = "Something went wrong."
	response = app.response_class(
			   	response=json.dumps( msg, indent=4),
			   	status=status,
			   	mimetype='application/json'
	)
	return response

if __name__ == '__main__':
	app.run('0.0.0.0')
