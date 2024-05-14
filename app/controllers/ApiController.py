from app import app
from flask import render_template, request, session, flash, redirect, url_for, abort
import requests

def show_all_product():
    api_url = app.config["API_URL"] + '/products'
    response = requests.get(api_url).json()
    
    if response['status']['code'] == 200:
        data = response["data"]
        return render_template("products.html", data = data)

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
            return render_template('index.html')
        elif response.status_code == 401:
            error = response.json()["status"]["message"]
        else:
            error = response.json()["status"]["message"]
    
    return render_template('login.html', error = error)

def logout():
    session.pop('token', None)
    flash("Logout Sukses")
    return redirect(url_for('login'))

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

def dashboard():
    token = session.get('token')
    if token:
        api_url = app.config["API_URL"] + '/products'
        response = requests.get(api_url).json()
        
        if response['status']['code'] == 200:
            data = response["data"]
            return render_template('dashboard.html', data = data)
    
    return redirect(url_for('login'))

def create_product(productId):
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

def update_product(productId):
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
        elif response['status']['code'] == 404:
            abort(404)
        else:
            abort(500)

    return redirect(url_for('login'))

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