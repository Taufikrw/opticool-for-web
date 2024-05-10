from app import app
from flask import render_template, request, jsonify
import requests

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/products', methods = ['GET'])
def show_products():
    api_url = app.config["API_URL"] + '/products'
    response = requests.get(api_url).json()
    
    if response['status']['code'] == 200:
        data = response["data"]
        return render_template("products.html", data = data)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        api_url = app.config["API_URL"] + '/login'

        login_data = {
            'email': email, 
            'password': password
        }
        response = requests.post(api_url, data=login_data)
        if response.status_code == 200:
            return render_template('index.html')
        elif response.status_code == 401:
            error = response.json()["status"]["message"]
        else:
            error = response.json()["status"]["message"]
    
    return render_template('login.html', error = error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        api_url = app.config["API_URL"] + '/register'

        new_data = {
            'name': name,
            'email': email, 
            'password': password
        }
        response = requests.post(api_url, data=new_data)
        if response.status_code == 200:
            return render_template('login.html')
        elif response.status_code == 409:
            error = response.json()["status"]["message"]
        else:
            error = response.json()["status"]["message"]
    
    return render_template('register.html', error = error)