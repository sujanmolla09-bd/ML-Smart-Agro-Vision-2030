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

import os
import io
import base64
from flask import Flask, send_file
from matplotlib.figure import Figure

# Flask অ্যাপ তৈরি
app = Flask(__name__)

# মূল ওয়েবসাইটের ঠিকানা (/)
@app.route('/')
def welcome():
    # যখন কেউ আপনার ওয়েবসাইটে ঢুকবে, তখন এই মেসেজটি দেখাবে
    html = """
    <html>
        <body>
            <h1>Welcome to ML-Smart-Agro-Vision-2030 by Sujan Molla!</h1>
            <p>Click the link below to see your data visualization:</p>
            <a href="/plot.png">View Plot</a>
        </body>
    </html>
    """
    return html

# ছবি দেখানোর জন্য একটি নতুন ঠিকানা (/plot.png)
@app.route('/plot.png')
def plot_png():
    # matplotlib ব্যবহার করে একটি ছবি তৈরি করা হচ্ছে
    fig = Figure(figsize=(4, 3), facecolor='w')
    axis = fig.subplots()
    ys = [198, 201, 205, 199, 202, 203, 200]
    xs = range(len(ys))
    axis.plot(xs, ys, '-')
    axis.fill_between(xs, ys, 195, where=(ys > 195), facecolor='g', alpha=0.6)
    axis.set_title("Sample Visualization")
    
    # ছবিটি মেমোরিতে সেভ করা হচ্ছে
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    
    # ব্রাউজারে ছবিটি পাঠানো হচ্ছে
    return send_file(output, mimetype='image/png')


if __name__ == "__main__":
    # Cloud Run-এর জন্য পোর্ট সেট করা
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

