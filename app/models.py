from . import db

class User(db.Model):
    __tablename__ = 'User'

    firebaseID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    shippingAddress = db.Column(db.String(100), nullable=True)
    invoiceAddress = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"User('{self.firebaseID}', '{self.email}', '{self.passwd}', '{self.shippingAddress}', '{self.invoiceAddress}')"

class Disc(db.Model):
    __tablename__ = 'Disc'

    idDisc = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    title = db.Column(db.String(100))
    format = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"Disc('{self.idDisc}', '{self.label}', '{self.title}', '{self.format}', {self.price})"

# Artist Model
class Artist(db.Model):
    __tablename__ = 'Artist'

    idArtist = db.Column(db.Integer, primary_key=True)
    nameArtist = db.Column(db.String(100))

    def __repr__(self):
        return f"Artist('{self.idArtist}', '{self.nameArtist}')"

class Genre(db.Model):
    __tablename__ = 'Genre'

    idGenre = db.Column(db.Integer, primary_key=True)
    nameGenre = db.Column(db.String(100))

    def __repr__(self):
        return f"Genre('{self.idGenre}', '{self.nameGenre}')"


class Song(db.Model):
    __tablename__ = 'Song'

    idSong = db.Column(db.Integer, primary_key=True)
    songName = db.Column(db.String(100))
    releaseDate = db.Column(db.Date)

    def __repr__(self):
        return f"Song('{self.idSong}', '{self.songName}', '{self.releaseDate}')"


class CartItem(db.Model):
    __tablename__ = 'CartItem'

    idCartItem = db.Column(db.Integer, primary_key=True)
    firebaseID = db.Column(db.Integer, db.ForeignKey('User.firebaseID'))
    discItem = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f"CartItem('{self.idCartItem}', '{self.firebaseID}', '{self.discItem}', {self.quantity})"

# SpotifyLikedSong Model
class SpotifyLikedSong(db.Model):
    __tablename__ = 'SpotifyLikedSong'

    idSpotifyLikedSong = db.Column(db.Integer, primary_key=True)
    firebaseID = db.Column(db.Integer, db.ForeignKey('User.firebaseID'))
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'))

    user = db.relationship('User', backref=db.backref('spotify_liked_songs', lazy=True))
    song = db.relationship('Song', backref=db.backref('spotify_liked_songs', lazy=True))

    def __repr__(self):
        return f"SpotifyLikedSong('{self.idSpotifyLikedSong}', '{self.firebaseID}', '{self.idSong}')"

# SongGenre Model
class SongGenre(db.Model):
    __tablename__ = 'SongGenre'

    idSongGenre = db.Column(db.Integer, primary_key=True)
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre'))
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'))

    genre = db.relationship('Genre', backref=db.backref('song_genres', lazy=True))
    song = db.relationship('Song', backref=db.backref('song_genres', lazy=True))

    def __repr__(self):
        return f"SongGenre('{self.idSongGenre}', '{self.idGenre}', '{self.idSong}')"

# DiscSong Model
class DiscSong(db.Model):
    __tablename__ = 'DiscSong'

    idDiscSong = db.Column(db.Integer, primary_key=True)
    idDisc = db.Column(db.Integer, db.ForeignKey('Disc.idDisc'))
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'))

    disc = db.relationship('Disc', backref=db.backref('disc_songs', lazy=True))
    song = db.relationship('Song', backref=db.backref('disc_songs', lazy=True))

    def __repr__(self):
        return f"DiscSong('{self.idDiscSong}', '{self.idDisc}', '{self.idSong}')"

# SongArtistFeature Model
class SongArtistFeature(db.Model):
    __tablename__ = 'SongArtistFeature'

    idSongArtistFeature = db.Column(db.Integer, primary_key=True)
    idSong = db.Column(db.Integer, db.ForeignKey('Song.idSong'))
    idArtist = db.Column(db.Integer, db.ForeignKey('Artist.idArtist'))
    importance = db.Column(db.Integer)

    song = db.relationship('Song', backref=db.backref('song_artist_features', lazy=True))
    artist = db.relationship('Artist', backref=db.backref('song_artist_features', lazy=True))

    def __repr__(self):
        return f"SongArtistFeature('{self.idSongArtistFeature}', '{self.idSong}', '{self.idArtist}', {self.importance})"
