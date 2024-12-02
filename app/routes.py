from flask import Blueprint, request, jsonify, abort
from .models import User, Disc
from .utils import *
# from firebase_admin import auth  # Firebase Admin SDK for token verification
# from functools import wraps  # For creating a decorator

main_routes = Blueprint('main', __name__)


@main_routes.route('/about')
def about():
    return "This is the about page."


@main_routes.route('/discs', methods=['GET'])
def get_disc_by_id():
    disc_id = request.args.get('id', type=int)

    if disc_id is None:
        abort(400, description="Disc ID is required")
    disc = Disc.query.get(disc_id)
    if disc is None:
        abort(404, description="Disc not found")

    return jsonify({
        "idDisc": disc.idDisc,
        "label": disc.label,    
        "title": disc.title,   
        "format": disc.format,
        "price": disc.price
    })
