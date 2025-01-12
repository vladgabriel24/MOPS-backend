from flask import Blueprint, request, jsonify, abort, session
from .models import User, Disc
from .utils import *
from . import db
# from firebase_admin import auth  # Firebase Admin SDK for token verification
# from functools import wraps  # For creating a decorator

main_routes = Blueprint('main', __name__)


@main_routes.route('/about')
def about():
    # Check if the user is logged in by verifying the session
    if 'firebase_id' not in session:
        abort(403, description="Unauthorized access. Please log in.")
    return "This is the about page."


@main_routes.route('/discs', methods=['GET'])
def get_disc_by_id():
    
    discs = Disc.query.all()
    if discs is None:
        abort(500, description="Backend error")

    discs_list = [
        {
            "idDisc": disc.idDisc,
            "label": disc.label,
            "title": disc.title,
            "format": disc.format,
            "price": disc.price
        }
        for disc in discs
    ]

    return jsonify(discs_list)

@main_routes.route('/disc', methods=['GET'])
def get_disc_by_title():
    
    disc_title = request.args.get('title', type=str)
    print(disc_title)

    if disc_title is None:
        abort(400, description="Title is required")

    disc = Disc.query.filter(Disc.title == disc_title).first()
    print(disc)
    if disc is None:
        abort(500, description="Backend error")

    return jsonify({
        "idDisc": disc.idDisc,
        "label": disc.label,    
        "title": disc.title,   
        "format": disc.format,
        "price": disc.price
    })

@main_routes.route('/create-user', methods=['POST'])
def create_user():
    # Extracting user data from the incoming JSON request
    data = request.get_json()

    # Ensure all required fields are present
    firebase_id = data.get('firebaseID')
    shipping_address = data.get('shippingAddress')
    invoice_address = data.get('invoiceAddress')

    if not firebase_id:
        abort(400, description="Firebase ID is required")

    # Create a new user instance
    new_user = User(
        firebaseID=firebase_id,
        shippingAddress=shipping_address,
        invoiceAddress=invoice_address
    )

    db.session.add(new_user)

    # Try committing the user to the database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        abort(500, description="Error creating user: " + str(e))

    # Return the newly created user in the response
    return jsonify({
        'firebaseID': new_user.firebaseID,
        'shippingAddress': new_user.shippingAddress,
        'invoiceAddress': new_user.invoiceAddress,
        'idCartItem': new_user.idCartItem
    }), 201

@main_routes.route('/login', methods=['POST'])
def login():
    # Extract user data from the incoming JSON request
    data = request.get_json()

    firebase_id = data.get('firebaseID')

    # Check if the firebase_id is provided
    if not firebase_id:
        abort(400, description="Firebase ID is required")

    # Check if the firebase_id exists in the database
    user = User.query.filter_by(firebaseID=firebase_id).first()

    if not user:
        abort(404, description="User not found")

    # Store the firebase_id in the session (to keep the user logged in)
    session['firebase_id'] = user.firebaseID

    return jsonify({
        'message': 'User logged in successfully',
        'firebaseID': user.firebaseID
    }), 200

@main_routes.route('/logout', methods=['POST'])
def logout():
    # Clear the session to log out the user
    session.pop('firebase_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200