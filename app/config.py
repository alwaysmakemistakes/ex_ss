import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_2184_123:12345678@std-mysql.ist.mospolytech.ru/std_2184_123'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')