from app import app
from flask import render_template, request, session, redirect, url_for, flash
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
            session["token"] = response.json()["data"]["access_token"]
            return render_template('profile.html')
        elif response.status_code == 401:
            error = response.json()["status"]["message"]
        else:
            error = response.json()["status"]["message"]
    
    return render_template('login.html', error = error)

@app.route('/logout', methods = ['GET'])
def revoke_user():
    session.pop('token', None)
    flash("Logout Sukses")
    return redirect(url_for('login'))

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
            flash(response.json()["status"]["message"])
            return render_template('login.html')
        elif response.status_code == 409:
            error = response.json()["status"]["message"]
        else:
            error = response.json()["status"]["message"]
    
    return render_template('register.html', error = error)

@app.route('/profile', methods = ['GET'])
def profile():
    token = session.get('token')
    api_url = app.config["API_URL"] + '/profile'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return render_template('profile.html', user = response.json()["data"])
    else:
        return redirect(url_for('login'))

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    token = session.get('token')
    if token:
        api_url = app.config["API_URL"] + '/products'
        response = requests.get(api_url).json()
        
        if response['status']['code'] == 200:
            data = response["data"]
            return render_template('dashboard.html', data = data)
    
    return redirect(url_for('login'))

@app.route('/products/create', methods = ['GET', 'POST'])
def add_item():
    token = session.get('token')
    if token:
        error = None
        if request.method == 'POST':
            link = request.form.get('link')
            name = request.form.get('name')
            brand = request.form.get('brand')
            price = request.form.get('price')
            gender = request.form.get('gender')
            picture = request.files['picture']
            picture_content = picture.read()
            
            new_product = {
                'link': link,
                'name': name,
                'brand': brand,
                'price': price,
                'gender': gender
            }
            files = {'picture': (picture.filename, picture_content)}

            api_url = app.config["API_URL"] + '/products/create'
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(api_url, data=new_product, files=files, headers=headers)
            if response.status_code == 200:
                flash(response.json()["status"]["message"])
                return redirect(url_for('dashboard'))
            else:
                error = response.json()["status"]["message"]

        return render_template('create.html', error = error)
    return redirect(url_for('login'))

@app.route('/products/<productId>/update', methods = ['GET', 'POST'])
def update_product_db(productId):
    token = session.get("token")
    if token:
        api_url = app.config["API_URL"] + '/products/' + productId
        response = requests.get(api_url).json()

        if response['status']['code'] == 200:
            data = response["data"]
            if request.method == 'POST':
                link = request.form.get('link')
                name = request.form.get('name')
                brand = request.form.get('brand')
                price = request.form.get('price')
                gender = request.form.get('gender')
                picture = request.files['picture']
                picture_content = picture.read()
                
                update_product = {
                    'link': link,
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'gender': gender
                }
                files = {'picture': (picture.filename, picture_content)}

                headers = {
                    "Authorization": f"Bearer {token}"
                }
                response = requests.put(api_url, data=update_product, files=files, headers=headers)
                if response.status_code == 200:
                    flash(response.json()["status"]["message"])
                    return redirect(url_for('dashboard'))
                else:
                    error = response.json()["status"]["message"]

            return render_template("update.html", data = data)
        return "404"

    return redirect(url_for('login'))

@app.route('/products/<productId>/delete', methods = ['GET'])
def delete_product(productId):
    token = session.get("token")
    if token:
        api_url = app.config["API_URL"] + '/products/' + productId
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.delete(api_url, headers=headers)
        if response.status_code == 200:
            flash(response.json()["status"]["message"])
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))