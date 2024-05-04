from app.models.users import Users

from app import app, response, db
from flask import request

def save():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users(
            name = name,
            email = email,
        )
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.success({}, "Create user successfully")

    except Exception as e:
        return response.error(str(e), 500)