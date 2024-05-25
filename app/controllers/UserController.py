from app.models.users import Users

from app import app, response, db
from flask import request
from flask_jwt_extended import *

import datetime

def save():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')

        user = Users.query.filter_by(email=email).first()
        if user:
            return response.error("Email already registered", 409)

        user = Users(
            name = name,
            email = email,
            birthday = birthday,
            gender = gender
        )
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.success({}, "Create user successfully")

    except Exception as e:
        return response.error(str(e), 500)

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if not user:
            return response.error('Account not found', 404)
        
        if not user.checkPassword(password):
            return response.error("Email and Password doesn't match!", 401)

        data = singleObject(user)
        expires = datetime.timedelta(days=1)
        expires_refresh = datetime.timedelta(days=3)
        access_token = create_access_token(data, fresh=True, expires_delta= expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data" : data,
            "access_token" : access_token,
            "refresh_token" : refresh_token,
        }, "Login successful!")

    except Exception as e:
        return response.error(str(e), 500)

def showUser():
    try:
        current_user = get_jwt_identity()
        return response.success(current_user, "Success get user")
    
    except Exception as e:
        return response.error(str(e), 500)

def singleObject(data):
    data = {
        'id' : data.id,
        'name' : data.name,
        'email' : data.email,
        'gender' : data.gender,
        'birthday' : data.birthday
    }

    return data