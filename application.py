from helpers.http_helpers import parse_url, parse_edit_form_data
import json, pprint

from flask import Flask, url_for, render_template, request
from flask import redirect, flash, jsonify

import database_controller as db
from database.database_helpers import url_name

# # Initializes python shell to interface with database
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Artist, ArtistGenre, Genre
# from database_setup import Influence, TopSongs

# # Connect to database
# engine = create_engine('sqlite:///catalog.db')
# Base.metadata.bind = engine

# # Establish database connection session
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

app = Flask(__name__)

# Define number of recent additions to display on catalog homepage
MAX_RECENT_ADDITIONS = 5


@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def catalog():
    """ Displays HTML tempplate for catalog homepage """
    genres = db.db_get_all_genres()
    recent_items = db.db_get_recent_additions(MAX_RECENT_ADDITIONS)
    return render_template('catalog.html',
                           genres=genres,
                           recent_items=recent_items)


# Artist CRUD Routes

@app.route('/artist/<int:artist>/')
@app.route('/artist/<artist>/')
def artist(artist):
    """ Displays artist page by artist database id """
    artist = db.db_get_artist(parse_url(artist))
    return render_template('artist.html', artist=artist)


@app.route('/artist/create/',
           methods=['GET', 'POST'])
def artist_create():
    """ Renders and processess form for creating artists """
    if request.method == 'POST':
        form_data = request.form
        for item in form_data:
            spotify_id = item
            break
        message = db.db_add_artist(spotify_id)
        if message[0] == 'add':
            artist = db.db_get_artist(message[1])

        obj = dict(artist_name=artist['name'],
                   spotify_id=spotify_id,
                   artist_url=url_for('artist', artist=artist['url_name']))
        return json.dumps(obj)
    else:
        return render_template('artist_create.html')


@app.route('/artist/edit/<int:artist>/',
           methods=['GET', 'POST'])
@app.route('/artist/edit/<artist>/',
           methods=['GET', 'POST'])
def artist_edit(artist):
    """ Edit database entry of a specific artist """
    artist = db.db_get_artist(parse_url(artist))
    if request.method == 'POST':
        form_data = parse_edit_form_data(request.form)
        pprint.pprint(form_data)
        db.db_update_artist(form_data, artist['art_id'])
        return redirect(url_for('artist', artist=artist['art_id']))
    # Prevent any artist genres from being printed as unchecked in view
    db_genres = db.db_get_all_genres()
    for artist_genre in artist['genres']:
        db_genres.remove(artist_genre)
    return render_template('artist_edit.html',
                           artist=artist,
                           db_genres=db_genres)


@app.route('/artist/delete/<int:artist>/',
           methods=['GET', 'POST'])
@app.route('/artist/delete/<artist>/',
           methods=['GET', 'POST'])
def artist_delete(artist):
    """ Delete an artist from the database """
    artist = db.db_get_artist(artist)
    if request.method == 'POST':
        db.db_delete_artist(artist['art_id'])
        return redirect(url_for('catalog'))
    return render_template('artist_delete.html', artist=artist)


# Genre CRUD routes

@app.route('/genre/<int:genre>/')
@app.route('/genre/<genre>/')
def genre(genre):
    """ Displays all artists corresponding to a specific genre """
    genre, artists = db.db_get_genre(parse_url(genre))
    return render_template('genre.html',
                           genre=genre,
                           artists=artists)


@app.route('/genre/create/')
def genre_create():
    """ Create a new genre in the database """
    radiohead = dict(name='Radiohead',
                     url_name='radiohead',
                     emergence='1990',
                     genres=['Rock', 'Alternative'],
                     top_songs=['No Surprises', 'Reckoner', 'Fake Plastic Trees'])
    seratones = dict(name='Seratones',
                     url_name='seratones',
                     emergence='2016',
                     genres=['Rock', 'Indie'],
                     top_songs=['Don\'t Need It', 'Necromancer', 'Chandelier'])
    artists = [radiohead, seratones]
    return render_template('genre_create.html', artists=artists)


@app.route('/genre/edit/<int:genre>/')
@app.route('/genre/edit/<genre>/')
def genre_edit(genre):
    """ Edit a specific genre """
    radiohead = dict(name='Radiohead',
                     art_id=1,
                     url_name='radiohead',
                     emergence='1990',
                     genres=['Rock', 'Alternative'],
                     top_songs=['No Surprises', 'Reckoner', 'Fake Plastic Trees'])
    seratones = dict(name='Seratones',
                     art_id=2,
                     url_name='seratones',
                     emergence='2016',
                     genres=['Rock', 'Indie'],
                     top_songs=['Don\'t Need It', 'Necromancer', 'Chandelier'])
    genre = dict(name='Alternative',
                 artists=[2])
    artists = [radiohead, seratones]
    return render_template('genre_edit.html',
                           artists=artists,
                           genre=genre)


@app.route('/genre/delete/<int:genre>/')
@app.route('/genre/delete/<genre>/')
def genre_delete(genre):
    """ Delete a specific genre """
    genre = dict(name='Alternative',
                 artists=[2])
    return render_template('genre_delete.html', genre=genre)


if __name__ == '__main__':
    app.secret_key = 'turtles'  # TODO: Change me for production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
