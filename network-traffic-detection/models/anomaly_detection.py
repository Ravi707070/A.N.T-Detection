import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_DIR = 'odels'
os.makedirs(MODEL_DIR, exist_ok=True)

def preprocess_data(filepath):
    data = pd.read_csv(filepath)
    data.fillna(method='ffill', inplace=True)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    data_id = os.path.basename(filepath).split('.')[0]
    joblib.dump(scaled_data, os.path.join(MODEL_DIR, f'{data_id}_data.pkl'))
    return data_id

def train_model(data_id):
    data_path = os.path.join(MODEL_DIR, f'{data_id}_data.pkl')
    data = joblib.load(data_path)
    model = IsolationForest(contamination=0.01)
    model.fit(data)
    model_path = os.path.join(MODEL_DIR, f'{data_id}_model.pkl')
    joblib.dump(model, model_path)
    return data_id

def detect_anomalies(file):
    # Load the CSV file
    df = pd.read_csv(file)
    # Preprocess the data
    data_id = preprocess_data(file)
    # Train the model
    train_model(data_id)
    # Load the model and data
    model_path = os.path.join(MODEL_DIR, f'{data_id}_model.pkl')
    data_path = os.path.join(MODEL_DIR, f'{data_id}_data.pkl')
    model = joblib.load(model_path)
    data = joblib.load(data_path)
    # Perform anomaly detection
    anomalies = model.predict(data)
    return anomalies.tolist()

if __name__ == "__main__":
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route('/detect_anomalies', methods=['POST'])
    def api_detect_anomalies():
        file = request.files['file']
        anomalies = detect_anomalies(file)
        return jsonify({'anomalies': anomalies})
