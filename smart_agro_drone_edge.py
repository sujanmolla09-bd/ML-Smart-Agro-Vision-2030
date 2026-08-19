import os
import pandas as pd
from flask import Flask, jsonify
from datetime import datetime

# Flask অ্যাপ তৈরি
app = Flask(__name__)

def main_gcp_pipeline():
    """
    GCP Pipeline for Smart Agro Telemetry (Successfully Migrated from Snowflake)
    Processes drone & IoT sensor telemetry dynamically using Pandas.
    """
    # আপনার ড্রোনের লাইভ স্যাম্পল ডেটা স্ট্রাকচার
    telemetry_data = [
        {"sensor_id": "DRONE-01", "temperature": 28.5, "humidity": 75.2, "soil_moisture": 42.0, "timestamp": datetime.now().isoformat()},
        {"sensor_id": "DRONE-02", "temperature": 29.1, "humidity": 72.8, "soil_moisture": 40.5, "timestamp": datetime.now().isoformat()},
        {"sensor_id": "IOT-FIELD-A", "temperature": 27.8, "humidity": 78.0, "soil_moisture": 45.1, "timestamp": datetime.now().isoformat()}
    ]
    
    # ডেটাকে Pandas DataFrame-এ রূপান্তর (স্নোফ্লেক স্নোপার্কের বিকল্প হিসেবে)
    df = pd.DataFrame(telemetry_data)
    
    # ডেটা অ্যানালাইসিস এবং গড় (Average) মেট্রিকে রূপান্তর করা
    summary_df = df.groupby("sensor_id").agg(
        AVG_TEMP=("temperature", "mean"),
        AVG_HUMIDITY=("humidity", "mean")
    ).reset_index()
    
    # চূড়ান্ত ফলাফলকে ডিকশনারি ফরম্যাটে রূপান্তর (যাতে ক্লাউড সহজে প্রসেস করতে পারে)
    return summary_df.to_dict(orient="records")

# ওয়েবসাইটের মূল হোমপেজ রুট (/)
@app.route('/')
def run_pipeline():
    try:
        # স্নোফ্লেক ছাড়া সরাসরি জিসিপির ওপর ডেটা প্রসেস রান হচ্ছে
        result = main_gcp_pipeline()
        return jsonify({
            "status": "Success ✅", 
            "message": "Smart Agro Edge System is running directly on Google Cloud!", 
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "Failed ❌",
            "error": str(e)
        })

# ক্লাউড রান পোর্টের জন্য গেটওয়ে কানেকশন
if __name__ == "__main__":
    # Cloud Run-এর রানিং পোর্ট নির্ধারণ
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
