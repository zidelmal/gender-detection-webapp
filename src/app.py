# Import modules
import joblib
import numpy as np
import pandas as pd
from prediction.prediction import Prediction
from flask import (Flask, 
                   render_template, 
                   request,
                   send_file)

# Init some functions

# Init the flask server
app = Flask(__name__)


# Initialize the predictor
prediction = Prediction(request)

# Put some routes
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	try:
		data = prediction.prediction()
		return render_template('result.html',meta = data)
	except:
		return render_template('index.html')

@app.route("/getPrediction")
def getPlotCSV():
    return send_file(
        'static/media/data/prediction.csv',
        mimetype="text/csv",
        download_name='prediction.csv',
        as_attachment=True)

if __name__ == '__main__':
	app.run(debug=True)

