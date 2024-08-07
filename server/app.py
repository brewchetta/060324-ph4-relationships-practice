#!/usr/bin/env python3

from flask import request
from config import app, db
from models import Artist, Album, Song

@app.get('/')
def index():
    return "Hello world"



# ARTIST ROUTES ############################################################

@app.get('/artists')
def all_artists():
    # 1. Get all artists from the db
    artist_list = Artist.query.all()
    
    # 2. Convert into dictionaries
    artist_dicts = [ artist.to_dict( rules=("-albums",) ) for artist in artist_list ]

    # 3. Send a response to the client
    return artist_dicts, 200


@app.get('/artists/<int:id>')
def get_artist(id):
    # 1. SQLALchemy query to get an artist by their id
    found_artist = Artist.query.where(Artist.id == id).first()

    # 2. Conditional if the artist exists
    if found_artist:
    
        # 2a. Return the found artist
        return found_artist.to_dict(), 200
    
    # 3. If no artist then...
    else:

        # 3a. Return an error message with the 404 status code
        return { "error": "Not found" }, 404
    

@app.post('/artists')
def create_artist():
    # 1. Get the information from the body/json
    data = request.json # <<<< this is a dictionary

    # start the try
    try:

        # 2. Make a new artist instance
        new_artist = Artist(name=data['name'])

        # 3. Put it in the database
        db.session.add(new_artist)
        db.session.commit()

        # 4. Return the new artist to the client
        return new_artist.to_dict(), 201

    # if anything goes wrong...
    except Exception as e:
        
        # Send a response letting the client know WE THEY FAILED
        return { 'error': str(e) }, 400
    

@app.patch('/artists/<int:id>')
def update_artist(id):
    # 1. Get the artist
    found_artist = Artist.query.where(Artist.id == id).first()

    # 2. Conditional for it we get / don't get the artist
    if found_artist:

        # 3. If we have the artist then get the body
        data = request.json

        # Start try in case anything bad happens like invalid data
        try:

            # 4. Loop through each key in the body
            for key in data:

                # 4a. Set the attribute for each key we got
                setattr( found_artist, key, data[key] )

            # 5. Push changes to the db
            db.session.add( found_artist )
            db.session.commit()

            # 6. Send the changed artist back to the client
            return found_artist.to_dict(), 202
        
        # Catch any errors due to invalid data
        except Exception as e:

            return { 'error': str(e) }, 400

    # If no artist then send back a 404
    else:

        return { 'error': 'Not found' }, 404
    

@app.delete('/artists/<int:id>')
def delete_artist(id):

    # 1. Grab that artist
    found_artist = Artist.query.where(Artist.id == id).first()

    # 2. Conditional in case we find / don't find an artist
    if found_artist:
        
        # 3. Delete the artist
        db.session.delete(found_artist)
        db.session.commit()

        return {}, 204

    # If artist not found return our standard 404
    else:
        return { 'error': 'Not found' }, 404



# ALBUM ROUTES ############################################################

@app.get('/albums')
def all_albums():
    album_list = Album.query.all()
    album_dicts = [ album.to_dict() for album in album_list ]
    return album_dicts, 200


@app.get('/albums/<int:id>')
def get_album(id):
    found_album = Album.query.where(Album.id == id).first()
    if found_album:
        return found_album.to_dict(), 200
    else:
        return {'error': 'Not found'}, 404



# SONG ROUTES ############################################################

@app.get('/songs')
def all_songs():
    song_list = Song.query.all()
    song_dicts = [ song.to_dict() for song in song_list ]
    return song_dicts, 200


@app.get('/songs/<int:id>')
def get_song(id):
    found_song = Song.query.where(Song.id == id).first()
    if found_song:
        return found_song.to_dict(), 200
    else:
        return {'error': 'Not found'}, 404
    

@app.post('/songs')
def create_song():
    data = request.json
    try:
        new_song = Song(title=data['title'], album_id=data['album_id'])
        db.session.add(new_song)
        db.session.commit()
        return new_song.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 400
    

@app.patch('/songs/<int:id>')
def update_song(id):
    found_song = Song.query.where(Song.id == id).first()

    if found_song:
        data = request.json
        try:
            for key in data:
                setattr(found_song, key, data[key])
            db.session.add(found_song)
            db.session.commit()

            return found_song.to_dict(), 202
        except Exception as e:
            return { 'error': str(e) }, 400

    else:
        return {'error': 'Not found'}, 404
    

@app.delete('/songs/<int:id>')
def delete_song(id):
    found_song = Song.query.where(Song.id == id).first()

    if found_song:
        db.session.delete(found_song)
        db.session.commit()
        return {}, 204
    
    else:
        return { 'error': 'Not found' }, 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
