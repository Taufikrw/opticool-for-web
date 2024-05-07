from app import app
from flask import render_template
import requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def show_products():
    api_url = 'http://127.0.0.1:5000/api/products'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()["data"]
        return render_template("products.html", data = data)
    else:
        return f"Error: {response.status_code}"