DROP DATABASE MOPS;
CREATE DATABASE MOPS;
USE MOPS;

CREATE TABLE Disc(
    idDisc INT, -- Primary Key
    label VARCHAR(100),
    title VARCHAR(100),
    format VARCHAR(100),
    price INT
);

CREATE TABLE Artist(
    idArtist INT, -- Primary Key
    nameArtist VARCHAR(100)
);

CREATE TABLE Genre(
    idGenre INT, -- Primary Key
    nameGenre VARCHAR(100)
);

CREATE TABLE CartItem(
    idCartItem INT, -- Primary Key
    discItem VARCHAR(100),
    quantity INT
);

CREATE TABLE Song(
    idSong INT, -- Primary Key
    songName VARCHAR(100),
    releaseDate DATE
);

CREATE TABLE User(
    firebaseID VARCHAR(100), -- Primary Key
    shippingAddress VARCHAR(100),
    invoiceAddress VARCHAR(100),
    idCartItem INT -- Foreign Key referencing CartItem.idCartItem
);

CREATE TABLE SpotifyLikedSong(
    idSpotifyLikedSong INT, -- Primary Key
    firebaseID INT, -- Foreign Key referencing User.firebaseID
    idSong INT -- Foreign Key referencing Song.idSong
);

CREATE TABLE SongGenre(
    idSongGenre INT, -- Primary Key
    idGenre INT, -- Foreign Key referencing Genre.idGenre
    idSong INT -- Foreign Key referencing Song.idSong
);

CREATE TABLE DiscSong(
    idDiscSong INT, -- Primary Key
    idDisc INT, -- Foreign Key referencing Disc.idDisc
    idSong INT -- Foreign Key referencing Song.idSong
);

CREATE TABLE SongArtistFeature(
    idSongArtistFeature INT, -- Primary Key
    idSong INT, -- Foreign Key referencing Song.idSong
    idArtist INT, -- Foreign Key referencing Artist.idArtist
    importance INT
);