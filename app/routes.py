from app import app
from app.controllers import EyeglassesController

@app.route('/products', methods = ['GET'])
def get_products():
    return EyeglassesController.index()

@app.route('/products/<productId>', methods = ['GET'])
def detail_product(productId):
    return EyeglassesController.detail(productId)

@app.route('/products/create', methods = ['POST'])
def create_product():
    return EyeglassesController.save()