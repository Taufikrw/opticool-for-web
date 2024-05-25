from app.models.eyeglasses import Eyeglasses

from app import app, db, response, uploadconfig, model, class_names
from flask import request
from werkzeug.utils import secure_filename

import os, uuid, cv2
import tensorflow as tf
import numpy as np

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
        if 'picture' not in request.files:
            return response.error("No file part in the request", 400)

        linkPic1 = request.files.get('picture')
        if linkPic1.filename == '':
            return response.error("No selected file", 400)
        if linkPic1 and uploadconfig.allowed_file(linkPic1.filename):
            uid = uuid.uuid4()
            filetype = linkPic1.filename.rsplit('.', 1)[1].lower()
            renamefile = str(uid) + '.' + filetype
            linkPic1.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))
            data = Eyeglasses(
                link = link, 
                name = name, 
                brand = brand, 
                price = price, 
                gender = gender,
                linkPic1 = renamefile
            )
            db.session.add(data)
            db.session.commit()
        else:
            return response.error("Invalid file type", 400)
        
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
        
        linkPic1 = request.files.get('picture')
        if linkPic1:
            old_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], product.linkPic1)
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)
            linkPic1.save(os.path.join(app.config['UPLOAD_FOLDER'], product.linkPic1))

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

        picture_path = os.path.join(app.config['UPLOAD_FOLDER'], product.linkPic1)
        if os.path.exists(picture_path):
            os.remove(picture_path)
        
        db.session.delete(product)
        db.session.commit()

        return response.success({}, "Product deleted successfully")

    except Exception as e:
        return response.error(str(e), 500)

def predict():
    try:
        image_file = request.files["image"]

        if image_file and uploadconfig.allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_ML'], filename)
            image_file.save(filepath)

            image = cv2.imread(filepath)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            resized_image = tf.image.resize(image, (250, 190))
            normalized_image = resized_image / 255.0
            input_data = np.expand_dims(normalized_image, axis=0)

            predictions = model.predict(input_data)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class = class_names[predicted_class_index]

            return response.success(predicted_class, "Predict Successfully")
        else:
            return response.error("Invalid file format. Please upload a PNG, JPG, or JPEG image.", 400)

    except Exception as e:
        return response.error(str(e), 500)

def rekomendation(faceshape):
    product = Eyeglasses.query.filter_by(faceShape = faceshape).limit(5).all()
    return formatArray(product)

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