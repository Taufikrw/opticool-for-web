from app import db, cipher_suite

class EncryptedField(db.TypeDecorator):
    impl = db.String

    def __init__(self, *args, **kwargs):
        super(EncryptedField, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = cipher_suite.encrypt(value.encode('utf-8')).decode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
        return value