import os
from flask import Flask

# Flask অ্যাপ তৈরি
app = Flask(__name__)

# মূল ওয়েবসাইটের ঠিকানা (/)
@app.route('/')
def hello_world():
    # যখন কেউ আপনার ওয়েবসাইটে ঢুকবে, তখন এই মেসেজটি দেখাবে
    message = "Welcome to ML-Smart-Agro-Vision-2030 by Sujan Molla!"
    return f'<h1>{message}</h1>'

if __name__ == "__main__":
    # Cloud Run-এর জন্য পোর্ট সেট করা
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

