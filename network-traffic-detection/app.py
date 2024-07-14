from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Set the maximum allowed payload to 200MB.
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB

#  data store for analysis data and comments
historical_data_store = {}

@app.route('/api/traffic-data', methods=['POST'])
def upload_and_analyze_traffic_data():
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return jsonify({"status": "error", "message": "Only CSV files are allowed"}), 400

    #  reading analyzing the file
    traffic_data = file.read()

    # analysis result  anomaly detection
    file_size = len(traffic_data)
    anomaly_percentage = round(random.uniform(0, 100), 2)  # anomaly detection percentage
    analysis_result = f"Analysis result for file size: {file_size} bytes"
    analysis_id = len(historical_data_store) + 1

    # Store analysis result  data store
    historical_data_store[analysis_id] = {
        "file_name": file.filename,
        "file_size": file_size,
        "result": analysis_result,
        "anomaly_percentage": anomaly_percentage,
        "comments": []
    }

    return jsonify({
        "status": "success",
        "analysisId": analysis_id,
        "results": analysis_result,
        "anomalyPercentage": anomaly_percentage
    })

@app.route('/api/analysis/<int:analysis_id>/comment', methods=['POST'])
def add_comment(analysis_id):
    comment = request.json.get('comment')
    if analysis_id not in historical_data_store:
        return jsonify({"status": "error", "message": "Invalid analysisId"}), 400
    
    historical_data_store[analysis_id]['comments'].append(comment)
    return jsonify({"status": "success", "comments": historical_data_store[analysis_id]['comments']})

@app.route('/api/analyses', methods=['GET'])
def list_historical_analyses():
    analyses = [
        {
            "analysisId": k,
            "fileName": v["file_name"],
            "fileSize": v["file_size"],
            "result": v["result"],
            "anomalyPercentage": v["anomaly_percentage"],
            "comments": v["comments"]
        }
        for k, v in historical_data_store.items()
    ]
    return jsonify({"analyses": analyses})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)