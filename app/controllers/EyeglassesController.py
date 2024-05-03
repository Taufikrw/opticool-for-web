from app.models.eyeglasses import Eyeglasses

from app import app, db, response
from flask import request

def index():
    try:
        products = Eyeglasses.query.all()
        data = formatArray(products)

        return response.success(data, "Success fetching the Data")

    except Exception as e:
        return response.error(str(e), 500)

def detail(id):
    try:
        product = Eyeglasses.query.filter_by(id = id).first()
        if not product:
            return response.error("Data not Found", 404)
            
        data = singleObject(product)

        return response.success(data, "Success fetching the Data")
    
    except Exception as e:
        return response.error(str(e), 500)

def save():
    try:
        link = request.form.get('link')
        name = request.form.get('name')
        brand = request.form.get('brand')
        price = request.form.get('price')
        gender = request.form.get('gender')

        data = Eyeglasses(
            link = link, 
            name = name, 
            brand = brand, 
            price = price, 
            gender = gender
        )
        db.session.add(data)
        db.session.commit()
        
        new_product = Eyeglasses.query.filter_by(id = data.id).first()
        data = singleObject(new_product)
        return response.success(data, "Data added successfully")
    except Exception as e:
        return response.error(str(e), 500)

def edit(id):
    try:
        link = request.form.get('link')
        name = request.form.get('name')
        brand = request.form.get('brand')
        price = request.form.get('price')
        gender = request.form.get('gender')

        product = Eyeglasses.query.filter_by(id = id).first()
        if not product:
            return response.error("Data Not Found", 404)

        product.link = link
        product.name = name
        product.brand = brand
        product.price = price
        product.gender = gender

        db.session.commit()
        data = singleObject(product)

        return response.success(data, "Data updated successfully")
    except Exception as e:
        return response.error(str(e), 500)

def delete(id):
    try:
        product = Eyeglasses.query.filter_by(id = id).first()
        if not product:
            return response.error("Data Not Found", 404)
        
        db.session.delete(product)
        db.session.commit()

        return response.success({}, "Product deleted successfully")

    except Exception as e:
        return response.error(str(e), 500)

def formatArray(datas):
    arr = []

    for i in datas:
        arr.append(singleObject(i))

    return arr

def singleObject(data):
    data = {
        'id' : data.id,
        'link' : data.link,
        'name' : data.name,
        'brand' : data.brand,
        'faceShape' : data.faceShape,
        'price' : data.price,
        'gender' : data.gender,
        'frameColour' : data.frameColour,
        'frameShape' : data.frameShape,
        'frameStyle' : data.frameStyle,
        'linkPic1' : data.linkPic1,
        'linkPic2' : data.linkPic2,
        'linkPic3' : data.linkPic3,
        'frameMaterial' : data.frameMaterial,
    }

    return data