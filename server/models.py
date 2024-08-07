from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

# Artist ---< Albums ---< Songs
# no fk     artist_id   album_id

class Artist(db.Model):
    
    __tablename__ = 'artist_table'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String, nullable=False )

    # RELATIONSHIPS

    albums = db.relationship('Album', back_populates='artist')
    # arg 1 = name of the other class
    # arg 2 = back populates --> the name of the method in the other class pointing to this class

    songs = association_proxy('albums', 'songs')
    # arg 1 = relationship name we're going through
    # arg 2 = the relationship that brings us to our final destination


class Album(db.Model):
    
    __tablename__ = 'album_table'

    id = db.Column( db.Integer, primary_key=True )
    title = db.Column( db.String )
    date_of_release = db.Column( db.DateTime )

    artist_id = db.Column( db.Integer, db.ForeignKey('artist_table.id') )

    # RELATIONSHIPS

    artist = db.relationship('Artist', back_populates='albums')

    songs = db.relationship('Song', back_populates='album')


class Song(db.Model):
    
    __tablename__ = 'song_table'

    id = db.Column( db.Integer, primary_key=True )
    title = db.Column( db.String )

    album_id = db.Column( db.Integer, db.ForeignKey('album_table.id') )

    # RELATIONSHIPS

    album = db.relationship('Album', back_populates='songs')

    artist = association_proxy('album', 'artist')