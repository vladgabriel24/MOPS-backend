from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://admin:password@172.24.80.1/MOPS?collation=utf8mb4_general_ci') # Replace with your ip 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Replace with a strong secret key for production

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app