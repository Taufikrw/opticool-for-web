from app import app, response
from app.controllers import EyeglassesController, UserController
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

@app.route('/protected', methods = ['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Success get user')

@app.route('/products', methods = ['GET'])
def get_products():
    return EyeglassesController.index()

@app.route('/products/<productId>', methods = ['GET'])
def detail_product(productId):
    return EyeglassesController.detail(productId)

@app.route('/products/<productId>', methods = ['PUT', 'DELETE'])
@jwt_required()
def update_product(productId):
    if request.method == 'PUT':
        return EyeglassesController.edit(productId)
    
    elif request.method == 'DELETE':
        return EyeglassesController.delete(productId)

@app.route('/products/create', methods = ['POST'])
def create_product():
    return EyeglassesController.save()

@app.route('/register', methods = ['POST'])
def create_user():
    return UserController.save()

@app.route('/login', methods = ['POST'])
def login():
    return UserController.login()