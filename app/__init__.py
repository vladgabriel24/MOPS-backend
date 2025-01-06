from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import firebase_admin 
from firebase_admin import credentials

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://admin:password@172.24.80.1/MOPS?collation=utf8mb4_general_ci')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    icred = credentials.Certificate("/mnt/c/Users/Athanasia/Desktop/Master/MOPS-proiect/app/proiect-react-6e4d1-firebase-adminsdk-9kmra-0f6b5be962.json")
    firebase_admin.initialize_app(icred)

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
