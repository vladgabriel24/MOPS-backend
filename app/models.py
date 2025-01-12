from . import db

class User(db.Model):
    __tablename__ = 'user'

    firebaseID = db.Column(db.Integer, primary_key=True)
    shippingAddress = db.Column(db.String(100), nullable=True)
    invoiceAddress = db.Column(db.String(100), nullable=True)
    idCartItem = db.Column(db.Integer, db.ForeignKey('cartitem.idCartItem'), nullable=True)

    # Relationship with CartItem
    cart_item = db.relationship('CartItem', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.firebaseID}', '{self.shippingAddress}', '{self.invoiceAddress}', {self.idCartItem})"


class Disc(db.Model):
    __tablename__ = 'disc'  

    idDisc = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    label = db.Column(db.String(100), nullable=True) 
    title = db.Column(db.String(100), nullable=True)  
    format = db.Column(db.String(100), nullable=True)  
    price = db.Column(db.Integer, nullable=True)  

    def __repr__(self):
        return f"Disc('{self.idDisc}', '{self.label}', '{self.title}', '{self.format}', {self.price})"
    
class Artist(db.Model):
    __tablename__ = 'artist'

    idArtist = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameArtist = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Artist('{self.idArtist}', '{self.nameArtist}')"


class Genre(db.Model):
    __tablename__ = 'genre'

    idGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nameGenre = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Genre('{self.idGenre}', '{self.nameGenre}')"


class CartItem(db.Model):
    __tablename__ = 'cartitem'

    idCartItem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discItem = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"CartItem('{self.idCartItem}', '{self.discItem}', {self.quantity})"

class Song(db.Model):
    __tablename__ = 'song'

    idSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    songName = db.Column(db.String(100), nullable=True)
    releaseDate = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Song('{self.idSong}', '{self.songName}', '{self.releaseDate}')"

class SpotifyLikedSong(db.Model):
    __tablename__ = 'spotifylikedsong'

    idSpotifyLikedSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebaseID = db.Column(db.Integer, db.ForeignKey('user.firebaseID'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('song.idSong'), nullable=False)

    # Relationship with User and Song
    user = db.relationship('User', backref='spotify_liked_songs', lazy=True)
    song = db.relationship('Song', backref='spotify_liked_songs', lazy=True)

    def __repr__(self):
        return f"SpotifyLikedSong('{self.idSpotifyLikedSong}', {self.firebaseID}, {self.idSong})"

class SongGenre(db.Model):
    __tablename__ = 'songgenre'

    idSongGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGenre = db.Column(db.Integer, db.ForeignKey('genre.idGenre'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('song.idSong'), nullable=False)

    # Relationships with Genre and Song
    genre = db.relationship('Genre', backref='song_genres', lazy=True)
    song = db.relationship('Song', backref='song_genres', lazy=True)

    def __repr__(self):
        return f"SongGenre('{self.idSongGenre}', {self.idGenre}, {self.idSong})"
    

class DiscSong(db.Model):
    __tablename__ = 'discsong'

    idDiscSong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idDisc = db.Column(db.Integer, db.ForeignKey('disc.idDisc'), nullable=False)
    idSong = db.Column(db.Integer, db.ForeignKey('song.idSong'), nullable=False)

    # Relationships with Disc and Song
    disc = db.relationship('Disc', backref='disc_songs', lazy=True)
    song = db.relationship('Song', backref='disc_songs', lazy=True)

    def __repr__(self):
        return f"DiscSong('{self.idDiscSong}', {self.idDisc}, {self.idSong})"

class SongArtistFeature(db.Model):
    __tablename__ = 'songartistfeature'

    idSongArtistFeature = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSong = db.Column(db.Integer, db.ForeignKey('song.idSong'), nullable=False)
    idArtist = db.Column(db.Integer, db.ForeignKey('artist.idArtist'), nullable=False)
    importance = db.Column(db.Integer, nullable=False)

    # Relationships with Song and Artist
    song = db.relationship('Song', backref='song_artist_features', lazy=True)
    artist = db.relationship('Artist', backref='song_artist_features', lazy=True)

    def __repr__(self):
        return f"SongArtistFeature('{self.idSongArtistFeature}', {self.idSong}, {self.idArtist}, {self.importance})"



