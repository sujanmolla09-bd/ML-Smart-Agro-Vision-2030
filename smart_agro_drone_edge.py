import os
import pandas as pd
from flask import Flask, jsonify
from datetime import datetime
from google.cloud import bigquery

# Flask অ্যাপ তৈরি
app = Flask(__name__)

# BigQuery ক্লায়েন্ট ও ডেটাবেস কনফিগারেশন
project_id = "ml-consumer-smart-agro-14ees"  # আপনার আসল প্রজেক্ট আইডি
dataset_id = "smart_agro_data"
table_id = "telemetry_logs"
client = bigquery.Client(project=project_id)

def main_gcp_pipeline():
    """
    GCP Pipeline for Smart Agro Telemetry with BigQuery
    Processes drone telemetry and permanently stores data.
    """
    # আপনার ড্রোনের স্যাম্পল ডেটা স্ট্রাকচার
    telemetry_data = [
        {"sensor_id": "DRONE-01", "temperature": 28.5, "humidity": 75.2, "soil_moisture": 42.0, "timestamp": datetime.now().isoformat()},
        {"sensor_id": "DRONE-02", "temperature": 29.1, "humidity": 72.8, "soil_moisture": 40.5, "timestamp": datetime.now().isoformat()},
        {"sensor_id": "IOT-FIELD-A", "temperature": 27.8, "humidity": 78.0, "soil_moisture": 45.1, "timestamp": datetime.now().isoformat()}
    ]
    
    # ডেটাকে Pandas DataFrame-এ রূপান্তর করা
    df = pd.DataFrame(telemetry_data)
    
    # BigQuery-তে ডেটা স্থায়ীভাবে ইনসার্ট করা (স্নোফ্লেকের বিকল্প)
    table_ref = client.dataset(dataset_id).table(table_id)
    errors = client.insert_rows_from_dataframe(table_ref, df)
    
    if errors:
        raise Exception(f"BigQuery insert errors: {errors}")

    # ড্রোনের গড় ডেটা অ্যানালাইসিস
    summary_df = df.groupby("sensor_id").agg(
        AVG_TEMP=("temperature", "mean"),
        AVG_HUMIDITY=("humidity", "mean")
    ).reset_index()
    
    return summary_df.to_dict(orient="records")

# ওয়েবসাইটের মূল হোমপেজ রুট (/)
@app.route('/')
def run_pipeline():
    try:
        result = main_gcp_pipeline()
        return jsonify({
            "status": "Success ✅", 
            "message": "Data successfully processed and permanently saved to Google BigQuery!", 
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "Failed ❌",
            "error": str(e)
        })

# ক্লাউড রান পোর্ট সেটআপ
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
