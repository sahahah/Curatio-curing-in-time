from flask import Flask, render_template, request, jsonify

import pandas as pd


import os
from symptoms import sympList, predd, rnd_forest
from joblib import load
from collections import defaultdict

model = load(r'C:\Users\91707\Desktop\notebook\random_forest.joblib')

os.environ['FLASK_ENV'] = 'development'
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')


symptoms2 = sympList


@app.route('/')
def index():
    return "Welcome to the Symptom Checker Apsspa"


@app.route('/symptom_form')
def symptom_checker():
    return render_template('symptom_form.html', symptoms2=sympList)


@app.route('/predict', methods=['POST'])
def predict():
    selected_symptoms = request.form.getlist('symptoms')
# Determine the number of total symptoms (based on sympList)
    total_symptoms = 17
    # Initialize inputsfin as a list of 0s with the same length as the total number of symptoms
    inputsfin = [0] * total_symptoms

    # Fill in the selected symptoms, but only up to the first 17
    for i, symptom in enumerate(selected_symptoms):
        if i >= total_symptoms:
            break
        if symptom in sympList:
            index = sympList.index(symptom)
            inputsfin[i] = symptom

    selected_symptoms_str = ", ".join(selected_symptoms)
    inputs2 = len(inputsfin)
    num_symptoms = len(sympList)
    # Call the predd function with input_args
    prediction = predd(rnd_forest, *inputsfin)
    # @app.route('/predict', methods=['POST'])
    return render_template('prediction_template.html', selected_symptoms=selected_symptoms_str, inputsfin=inputsfin, inputs2=inputs2, num_symptoms=num_symptoms, prediction=prediction)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.debug = True  # enable debug mode
    app.run()
