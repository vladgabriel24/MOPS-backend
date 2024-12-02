from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# import firebase_admin 
# from firebase_admin import credentials

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://admin:password@localhost/MOPS?collation=utf8mb4_general_ci')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

     # Initialize Firebase Admin SDK -> TO DOOO
    # firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS', 'path/to/your-firebase-adminsdk.json')

    # if not firebase_admin._apps:  # Ensure Firebase isn't initialized multiple times
    #     cred = credentials.Certificate(firebase_credentials_path)
    #     firebase_admin.initialize_app(cred)

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
