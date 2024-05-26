from app import db, bcrypt
from datetime import datetime
from app.models.encryptedfield import EncryptedField
    
class Users(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    name = db.Column(EncryptedField(250), nullable = False)
    email = db.Column(db.String(250), index = True, unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    birthday = db.Column(db.Date, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return '<Users {}>'.format(self.name)

    def setPassword(self, password):
        self.password = bcrypt.generate_password_hash(password)
    
    def checkPassword(self, password):
        return bcrypt.check_password_hash(self.password, password)