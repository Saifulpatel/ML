from flask import Blueprint, render_template, request, flash
import pickle
import numpy as np
import os
import pandas as pd

# Load all models from the models directory
model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
models = {}
model_accuracies = {  # Example accuracies (Replace with actual values)
    "Random Forest": 89.3,
    "Linear Regression": 78.5,
    "Support Vector Machine": 82.1,
    "Gradient Boosting": 91.2,
    "Neural Network": 94.8
}

if os.path.exists(model_dir):
    for file in os.listdir(model_dir):
        if file.endswith(".pkl"):
            model_name = file.replace(".pkl", "").replace("_", " ")
            with open(os.path.join(model_dir, file), 'rb') as model_file:
                models[model_name] = pickle.load(model_file)

print(f"✅ Loaded Models: {list(models.keys())}")


# Load dataset for exploration and column details
data_file = os.path.join(os.getcwd(), 'data', 'Weather.csv')
if os.path.exists(data_file):
    data = pd.read_csv(data_file)
    columns = data.columns.tolist()
    total_records = len(data)
else:
    data = None
    columns = []
    total_records = 0

feature_weights = {
    "Temperature": 35.2,
    "Humidity": 25.5,
    "Pressure": 39.3
}


# Define Blueprint
main = Blueprint('main', __name__)

# Load dataset for exploration (Safe Load)
data_path = os.path.join(os.getcwd(), 'data', 'Weather.csv')
data = pd.read_csv(data_path) if os.path.exists(data_path) else None

# Home Route
@main.route('/')
def index():
    return render_template('index.html')

# Prediction Route
@main.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if request.method == 'POST':
            required_features = ["temperature", "humidity", "pressure"]
            print(f"Form Data: {request.form}")
            input_values = []
            missing_features = []
            
            for feature in required_features:
                if feature in request.form and request.form[feature].strip():
                    try:
                        input_values.append(float(request.form[feature]))
                    except ValueError:
                        flash(f"Invalid value for {feature}", "error")
                        return render_template('predict.html', predictions=None)
                else:
                    missing_features.append(feature)
            
            if missing_features:
                flash(f"Missing input for: {', '.join(missing_features)}", "error")
                return render_template('predict.html', predictions=None)

            # Convert list to NumPy array
            input_data = np.array([input_values])
            print(f"Received input: {input_data}")

            # Get predictions from models
            predictions = {}
            for model_name, model in models.items():
                try:
                    predictions[model_name] = round(model.predict(input_data)[0], 2)
                    print(f"{model_name} predicted: {predictions[model_name]}")
                except Exception as e:
                    predictions[model_name] = f"Error: {str(e)}"
                    print(f"Error in {model_name}: {e}")

            return render_template('predict.html', predictions=predictions)

        return render_template('predict.html', predictions=None)

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        print(f"Error in prediction: {str(e)}")
        return render_template('predict.html', predictions=None)

# Data Exploration Route
@main.route('/data-exploration')
def data_exploration():
    if data is not None:
        summary = data.describe().to_html()
        column_info = data.dtypes.to_frame().to_html()
    else:
        summary = "<p>No dataset found</p>"
        column_info = "<p>No dataset available</p>"

    return render_template('data_exploration.html', summary=summary, column_info=column_info)

# About Route
@main.route('/about')
def about():
    try:
        return render_template(
            'about.html',
            model_accuracies=model_accuracies,
            total_records=total_records,
            columns=columns if columns else ["No data available"],
            feature_weights=feature_weights
        )
    except Exception as e:
        print(f"Error in about route: {str(e)}")
        return f"Error: {str(e)}", 500
