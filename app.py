# Import modules
import joblib
import numpy as np
import pandas as pd
from preprocess.preprocess import Preprocess
from flask import Flask, render_template, url_for, request

# Init the flask server
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

	# Initialize the pre-process
	process = Preprocess()

	# Call the model from the pikle file
	clf=joblib.load('ETC.pkl')

	if request.method == 'POST':
		# Get the inputs
		name = request.form['name']
		# Create a df with unique or multiple value
		data = pd.DataFrame(data={'name': name.split(',')})
		# Verfy the integrity of data
		data = data[data['name'].str.len()<=20].reset_index(drop=True)
		# Clean the data for prediction
		data = process.preprocess(data)
		# Make the data readable for the model
		X = np.asarray(data['encoded_name'].values.tolist())
		X = X.reshape(X.shape[0], X.shape[1]*X.shape[2])
		# Get my prediction
		data['gender'] = clf.predict(X)
		data['name'] = data['name'].str.capitalize()
	return render_template('result.html',meta = data)


if __name__ == '__main__':
	app.run(debug=True)

