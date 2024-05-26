from app import app
from app.controllers import ApiController

@app.route('/', methods = ['GET'])
def index():
    return ApiController.index()

@app.route('/products', methods = ['GET'])
def show_products():
    return ApiController.show_all_product()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return ApiController.login()

@app.route('/logout', methods = ['GET'])
def revoke_user():
    return ApiController.logout()

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return ApiController.register()

@app.route('/profile', methods = ['GET'])
def profile():
    return ApiController.profile()

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    return ApiController.dashboard()

@app.route('/products/create', methods = ['GET', 'POST'])
def add_item():
    return ApiController.create_product()

@app.route('/products/<productId>/update', methods = ['GET', 'POST'])
def update_product_db(productId):
    return ApiController.update_product(productId)

@app.route('/products/<productId>/delete', methods = ['GET'])
def delete_product(productId):
    return ApiController.delete_product(productId)

@app.route('/scan', methods = ['GET', 'POST'])
def scan_faceshape():
    return ApiController.scan_faceshape()