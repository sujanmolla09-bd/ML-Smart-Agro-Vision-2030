# বেস ইমেজ হিসেবে পাইথন 3.9 ব্যবহার করা হচ্ছে
FROM python:3.9-slim

# অ্যাপের জন্য একটি ফোল্ডার তৈরি করা হচ্ছে
WORKDIR /app

# বর্তমান ফোল্ডারের সব ফাইল /app ফোল্ডারে কপি করা হচ্ছে
COPY . /app

# requirements.txt ফাইলে থাকা লাইব্রেরিগুলো ইনস্টল করা হচ্ছে
RUN pip install --no-cache-dir -r requirements.txt

# অ্যাপটি gunicorn দিয়ে Cloud Run-এ চালানোর জন্য চূড়ান্ত কমান্ড
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 smart_agro_drone_edge:app
