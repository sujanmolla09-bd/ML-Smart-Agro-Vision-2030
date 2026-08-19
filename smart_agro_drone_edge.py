import os
from flask import Flask, jsonify
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, avg
from datetime import datetime

# --- Snowflake Connection Details (এই তথ্যগুলো আমরা পরে নিরাপদে যুক্ত করব) ---
connection_parameters = {
    "account": "YOUR_SNOWFLAKE_ACCOUNT",
    "user": "YOUR_SNOWFLAKE_USER",
    "password": "YOUR_SNOWFLAKE_PASSWORD",
    "role": "YOUR_SNOWFLAKE_ROLE",
    "warehouse": "YOUR_SNOWFLAKE_WAREHOUSE",
    "database": "YOUR_SNOWFLAKE_DATABASE",
    "schema": "YOUR_SNOWFLAKE_SCHEMA"
}

# Flask অ্যাপ তৈরি
app = Flask(__name__)

def main_snowflake_pipeline():
    """
    Snowflake Snowpark Pipeline for Smart Agro Telemetry
    """
    try:
        session = Session.builder.configs(connection_parameters).create()
        
        # Sample Telemetry Data
        telemetry_data = [
            {"sensor_id": "DRONE-01", "temperature": 28.5, "humidity": 75.2, "soil_moisture": 42.0, "timestamp": datetime.now()},
            {"sensor_id": "DRONE-02", "temperature": 29.1, "humidity": 72.8, "soil_moisture": 40.5, "timestamp": datetime.now()},
        ]
        
        df = session.create_dataframe(telemetry_data)
        
        table_name = "AGRO_TELEMETRY_LOGS"
        df.write.mode("append").save_as_table(table_name)
        
        summary_df = session.table(table_name).group_by("sensor_id").agg(
            avg(col("temperature")).alias("AVG_TEMP"),
            avg(col("humidity")).alias("AVG_HUMIDITY")
        )
        
        # ফলাফলকে JSON ফরম্যাটে রিটার্ন করা হচ্ছে
        return summary_df.to_json(2)
        
    except Exception as e:
        return {"error": str(e)}

# মূল ওয়েবসাইটের ঠিকানা (/)
@app.route('/')
def run_pipeline():
    result = main_snowflake_pipeline()
    return jsonify(result)

if __name__ == "__main__":
    # Cloud Run-এর জন্য পোর্ট সেট করা
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

