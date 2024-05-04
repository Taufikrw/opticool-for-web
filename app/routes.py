from app import app
from app.controllers import EyeglassesController, UserController
from flask import request

@app.route('/products', methods = ['GET'])
def get_products():
    return EyeglassesController.index()

@app.route('/products/<productId>', methods = ['GET', 'PUT', 'DELETE'])
def detail_product(productId):
    if request.method == 'GET':
        return EyeglassesController.detail(productId)
    
    elif request.method == 'PUT':
        return EyeglassesController.edit(productId)
    
    elif request.method == 'DELETE':
        return EyeglassesController.delete(productId)

@app.route('/products/create', methods = ['POST'])
def create_product():
    return EyeglassesController.save()

@app.route('/register', methods = ['POST'])
def create_user():
    return UserController.save()