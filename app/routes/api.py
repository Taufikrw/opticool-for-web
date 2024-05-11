from app import app, response
from app.controllers import EyeglassesController, UserController
from flask import request
from flask_jwt_extended import jwt_required

@app.route('/api/products', methods = ['GET'])
def get_products():
    return EyeglassesController.index()

@app.route('/api/products/<productId>', methods = ['GET'])
def get_detail_product(productId):
    return EyeglassesController.detail(productId)

@app.route('/api/products/<productId>', methods = ['PUT', 'DELETE'])
@jwt_required()
def update_product(productId):
    if request.method == 'PUT':
        return EyeglassesController.edit(productId)
    
    elif request.method == 'DELETE':
        return EyeglassesController.delete(productId)

@app.route('/api/products/create', methods = ['POST'])
@jwt_required()
def create_product():
    return EyeglassesController.save()

@app.route('/api/register', methods = ['POST'])
def create_user():
    return UserController.save()

@app.route('/api/login', methods = ['POST'])
def login_user():
    return UserController.login()

@app.route('/api/profile', methods = ['GET'])
@jwt_required()
def api_profile():
    return UserController.showUser()