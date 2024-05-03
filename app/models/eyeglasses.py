from app import db

class Eyeglasses(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    link = db.Column(db.String(255), nullable = False)
    name = db.Column(db.String(255), nullable = False)
    brand = db.Column(db.String(255), nullable = False)
    faceShape = db.Column(db.String(15), nullable = True)
    price = db.Column(db.String(10), nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    frameColour = db.Column(db.String(100), nullable = True)
    frameShape = db.Column(db.String(20), nullable = True)
    frameStyle = db.Column(db.String(50), nullable = True)
    linkPic1 = db.Column(db.String(255), nullable = True)
    linkPic2 = db.Column(db.String(255), nullable = True)
    linkPic3 = db.Column(db.String(255), nullable = True)
    frameMaterial = db.Column(db.String(100), nullable = True)

    def __repr__(self) -> str:
        return '<Eyeglasses {}>'.format(self.name)
