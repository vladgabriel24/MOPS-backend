from . import db

class User(db.Model):
    __tablename__ = 'User'

    firebaseID = db.Column(db.Integer, primary_key=True)
    shippingAddress = db.Column(db.String(100), nullable=True)
    invoiceAddress = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"User('{self.firebaseID}', '{self.shippingAddress}', '{self.invoiceAddress}', {self.idCartItem})"


class Disc(db.Model):
    __tablename__ = 'Disc'  

    idDisc = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    label = db.Column(db.String(100), nullable=True) 
    title = db.Column(db.String(100), nullable=True)  
    format = db.Column(db.String(100), nullable=True)  
    price = db.Column(db.Integer, nullable=True)  

    def __repr__(self):
        return f"Disc('{self.idDisc}', '{self.label}', '{self.title}', '{self.format}', {self.price})"
    
class Artist(db.Model):
    __tablename__ = 'Artist'

    idArtist = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameArtist = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Artist('{self.idArtist}', '{self.nameArtist}')"


class Genre(db.Model):
    __tablename__ = 'Genre'

    idGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameGenre = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Genre('{self.idGenre}', '{self.nameGenre}')"


class CartItem(db.Model):
    __tablename__ = 'CartItem'

    idCartItem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discItem = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    firebaseID = db.Column(db.Integer, db.ForeignKey('User.firebaseID'), nullable=True)

    # Relationship with User
    cart_item = db.relationship('User', backref='cart_item', lazy=True)


    def __repr__(self):
        return f"CartItem('{self.idCartItem}', '{self.discItem}', {self.quantity})"

class Song(db.Model):
    __tablename__ = 'Song'

    idSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    songName = db.Column(db.String(100), nullable=True)
    releaseDate = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Song('{self.idSong}', '{self.songName}', '{self.releaseDate}')"

class SpotifyLikedSong(db.Model):
    __tablename__ = 'SpotifyLikedSong'

    idSpotifyLikedSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebaseID = db.Column(db.Integer, db.ForeignKey('User.firebaseID'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'), nullable=False)

    # Relationship with User and Song
    user = db.relationship('User', backref='spotify_liked_songs', lazy=True)
    song = db.relationship('Song', backref='spotify_liked_songs', lazy=True)

    def __repr__(self):
        return f"SpotifyLikedSong('{self.idSpotifyLikedSong}', {self.firebaseID}, {self.idSong})"

class SongGenre(db.Model):
    __tablename__ = 'SongGenre'

    idSongGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'), nullable=False)

    # Relationships with Genre and Song
    genre = db.relationship('Genre', backref='song_genres', lazy=True)
    song = db.relationship('Song', backref='song_genres', lazy=True)

    def __repr__(self):
        return f"SongGenre('{self.idSongGenre}', {self.idGenre}, {self.idSong})"
    

class DiscSong(db.Model):
    __tablename__ = 'DiscSong'

    idDiscSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idDisc = db.Column(db.Integer, db.ForeignKey('Disc.idDisc'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'), nullable=False)

    # Relationships with Disc and Song
    disc = db.relationship('Disc', backref='disc_songs', lazy=True)
    song = db.relationship('Song', backref='disc_songs', lazy=True)

    def __repr__(self):
        return f"DiscSong('{self.idDiscSong}', {self.idDisc}, {self.idSong})"

class SongArtistFeature(db.Model):
    __tablename__ = 'SongArtistFeature'

    idSongArtistFeature = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'), nullable=False)
    idArtist = db.Column(db.Integer, db.ForeignKey('Artist.idArtist'), nullable=False)
    importance = db.Column(db.Integer, nullable=False)

    # Relationships with Song and Artist
    song = db.relationship('Song', backref='song_artist_features', lazy=True)
    artist = db.relationship('Artist', backref='song_artist_features', lazy=True)

    def __repr__(self):
        return f"SongArtistFeature('{self.idSongArtistFeature}', {self.idSong}, {self.idArtist}, {self.importance})"



