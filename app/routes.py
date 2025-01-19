from flask import Blueprint, request, jsonify, abort, session
from .models import *
from .utils import *
from . import db
from flask_cors import CORS
# from firebase_admin import auth  # Firebase Admin SDK for token verification
# from functools import wraps  # For creating a decorator

main_routes = Blueprint('main', __name__)
CORS(main_routes)  # Allow all origins


@main_routes.route('/about')
def about():
    # Check if the user is logged in by verifying the session
    if 'firebase_id' not in session:
        abort(403, description="Unauthorized access. Please log in.")
    return "This is the about page."


@main_routes.route('/discs', methods=['GET'])
def get_disc():
    
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

@main_routes.route('/search-disc-by-title', methods=['GET'])
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

@main_routes.route('/search-discs-by-artist', methods=['GET'])
def get_discs_by_artist():
    # Get the artist name from query parameters
    artist_name = request.args.get('artist', type=str)
    if not artist_name:
        abort(400, description="Artist parameter is required")
    # Query to find the artist
    artist = Artist.query.filter_by(nameArtist=artist_name).first()
    if artist is None:
        abort(404, description=f"No artist found with name '{artist_name}'")
    print(artist.nameArtist)
    # Query to find all songs by the artist
    song_ids = [feature.idSong for feature in artist.song_artist_features]

    # Query to find all discs containing these songs
    disc_ids = {disc_song.idDisc for disc_song in DiscSong.query.filter(DiscSong.idSong.in_(song_ids)).all()}

    # Retrieve all discs
    discs = Disc.query.filter(Disc.idDisc.in_(disc_ids)).all()
    if not discs:
        abort(404, description=f"No discs found for artist '{artist_name}'")

    # Return the results as JSON
    return jsonify([
        {
            "idDisc": disc.idDisc,
            "label": disc.label,
            "title": disc.title,
            "format": disc.format,
            "price": disc.price
        } for disc in discs
    ])

@main_routes.route('/search-discs-by-genre', methods=['GET'])
def get_discs_by_genre():
    # Get the genre name from query parameters
    genre_name = request.args.get('genre', type=str)
    if not genre_name:
        abort(400, description="Genre parameter is required")

    # Query to find the genre
    genre = Genre.query.filter_by(nameGenre=genre_name).first()
    if not genre:
        abort(404, description=f"No genre found with name '{genre_name}'")

    # Query to find all songs associated with the genre
    song_ids = [song_genre.idSong for song_genre in genre.song_genres]

    # Query to find all discs containing these songs
    disc_ids = {disc_song.idDisc for disc_song in DiscSong.query.filter(DiscSong.idSong.in_(song_ids)).all()}

    # Retrieve all discs
    discs = Disc.query.filter(Disc.idDisc.in_(disc_ids)).all()
    if not discs:
        abort(404, description=f"No discs found for genre '{genre_name}'")

    # Return the results as JSON
    return jsonify([
        {
            "idDisc": disc.idDisc,
            "label": disc.label,
            "title": disc.title,
            "format": disc.format,
            "price": disc.price
        } for disc in discs
    ])

@main_routes.route('/disc', methods=['GET'])
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

@main_routes.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    # Check if the user is logged in by verifying the session
    if 'firebase_id' not in session:
        abort(403, description="Unauthorized access. Please log in.")

    data = request.get_json()  
    
    disc_item = data.get('discItem')  
    quantity = data.get('quantity')  
    
    if not disc_item or not quantity:
        abort(400, description="Disc item and quantity are required")
    
    if quantity <= 0:
        abort(400, description="Quantity must be a positive integer")
    
    firebase_id = session['firebase_id']
    user = User.query.filter_by(firebaseID=firebase_id).first()

    if not user:
        abort(404, description="User not found")
    
    disc = Disc.query.filter_by(title=disc_item).first()
    if not disc:
        abort(404, description="Disc not found")
    
    new_cart_item = CartItem(firebaseID=firebase_id, discItem=disc_item, quantity=quantity)
    
    db.session.add(new_cart_item)
    db.session.commit()
    
    return jsonify({
        "message": "Item added to cart successfully",
        "cartItem": {
            "idCartItem": new_cart_item.idCartItem,
            "firebaseID": new_cart_item.firebaseID,
            "discItem": new_cart_item.discItem,
            "quantity": new_cart_item.quantity
        }
    }), 201  # Return HTTP 201 (Created) response

@main_routes.route('/delete-cart-item', methods=['DELETE'])
def delete_cart_item():
    # Check if the user is logged in by verifying the session
    if 'firebase_id' not in session:
        abort(403, description="Unauthorized access. Please log in.")
    
    # Get the cart item ID from the request
    cart_item_id = request.args.get('id', type=int)  # Assume the ID is passed as a query parameter
    
    # Validate the cart item ID
    if cart_item_id is None:
        abort(400, description="Cart item ID is required")
    
    # Retrieve the CartItem from the database
    cart_item = CartItem.query.get(cart_item_id)
    
    # Check if the CartItem exists
    if cart_item is None:
        abort(404, description="Cart item not found")
    
    # Ensure the CartItem belongs to the authenticated user (firebase_id check)
    if cart_item.firebaseID != session['firebase_id']:
        abort(403, description="You are not authorized to delete this item")
    
    # Delete the CartItem from the database
    db.session.delete(cart_item)
    db.session.commit()
    
    # Return a success response
    return jsonify({
        "message": "Cart item deleted successfully"
    }), 200

@main_routes.route('/update-cart-item', methods=['PUT'])
def update_cart_item_quantity():
    # Check if the user is logged in by verifying the session
    if 'firebase_id' not in session:
        abort(403, description="Unauthorized access. Please log in.")
    
    # Get the cart item ID and new quantity from the request
    cart_item_id = request.args.get('id', type=int)  # The cart item ID as a query parameter
    new_quantity = request.json.get('quantity')  # New quantity sent as JSON body
    
    # Validate cart item ID and new quantity
    if cart_item_id is None:
        abort(400, description="Cart item ID is required")
    
    if new_quantity is None or new_quantity <= 0:
        abort(400, description="Quantity must be greater than 0")

    # Retrieve the CartItem from the database
    cart_item = CartItem.query.get(cart_item_id)
    
    # Check if the CartItem exists
    if cart_item is None:
        abort(404, description="Cart item not found")
    
    # Ensure the CartItem belongs to the authenticated user (firebase_id check)
    if cart_item.firebaseID != session['firebase_id']:
        abort(403, description="You are not authorized to update this item")
    
    # Update the quantity
    cart_item.quantity = new_quantity
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return a success response
    return jsonify({
        "message": "Cart item quantity updated successfully",
        "idCartItem": cart_item.idCartItem,
        "new_quantity": cart_item.quantity
    }), 200

@main_routes.route('/songs', methods=['GET'])
def get_songs_by_disc():
    # Retrieve the disc_id from query parameters
    disc_id = request.args.get('disc_id', type=int)

    # If disc_id is not provided, return a bad request error
    if not disc_id:
        abort(400, description="Disc ID is required")

    # Query the DiscSong table to find all songs related to the given disc ID
    disc_songs = DiscSong.query.filter_by(idDisc=disc_id).all()
    
    # If no disc songs are found, return an error message
    if not disc_songs:
        abort(404, description=f"No songs found for Disc ID {disc_id}")

    # Get the song details
    songs = []
    for disc_song in disc_songs:
        song = Song.query.get(disc_song.idSong)
        if song:
            songs.append({
                "idSong": song.idSong,
                "songName": song.songName,
                "releaseDate": song.releaseDate.strftime('%Y-%m-%d')  # Format date if needed
            })
    
    # Return the list of songs
    return jsonify(songs)

