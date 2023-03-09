#ici sera dev la webApp du model
import joblib
import numpy as np
import pandas as pd
from preprocess.preprocess import Preprocess
from flask import Flask, render_template, url_for, request
print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

app = Flask(__name__)

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

	# Initialize the pre-process
	process = Preprocess()

	# Call the model from the pikle model
	clf=joblib.load('ETC.pkl')

	if request.method == 'POST':

		name = request.form['name']
		data = pd.DataFrame(data={'name': name.split(',')})
		# Verfy the integrity of data
		data = data[data['name'].str.len()<=20].reset_index(drop=True)
		# Clean the data for prediction
		data = process.preprocess(data)
		# Make the data readable for the model
		X = np.asarray(data['encoded_name'].values.tolist())
		X = X.reshape(X.shape[0], X.shape[1]*X.shape[2])

		# data['predited_gender']=clf.predict(X)
		# result = clf.predict(X)

		# Get my prediction
		data['gender'] = clf.predict(X)
	return render_template('result.html',meta = data)


if __name__ == '__main__':
	app.run(debug=True)

