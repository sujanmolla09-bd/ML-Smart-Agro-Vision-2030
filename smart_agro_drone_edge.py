# --- Google Cloud Run এর জন্য নতুন কোড ---
import os
from flask import Flask

# Flask অ্যাপ তৈরি
app = Flask(__name__)

# মূল ওয়েবসাইটের ঠিকানা (/)
@app.route('/')
def run_drone_code():
    # এখানে আপনার ড্রোন কোডের মূল ফাংশনটি কল করা হবে
    # উদাহরণস্বরূপ, আমরা একটি স্ট্যাটাস মেসেজ রিটার্ন করছি
    status_message = "Smart Agro Drone Edge System is running!"
    
    # আপনার ড্রোন থেকে পাওয়া ডেটা বা স্ট্যাটাস এখানে দেখানো যেতে পারে
    # drone_data = get_drone_telemetry()
    # return f"<h1>{status_message}</h1><p>Data: {drone_data}</p>"
    
    return f"<h1>{status_message}</h1>"

if __name__ == "__main__":
    # Cloud Run-এর জন্য পোর্ট সেট করা
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

