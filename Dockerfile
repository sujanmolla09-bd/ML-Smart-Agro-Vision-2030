# (আগের লাইনগুলো একই থাকবে)
...

# অ্যাপটি gunicorn দিয়ে চালানোর জন্য নতুন কমান্ড
CMD ["gunicorn", "-b", ":8080", "smart_agro_drone_edge:app"]
