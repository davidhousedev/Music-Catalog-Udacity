from helpers.url_helpers import parse_url
import json

from flask import Flask, url_for, render_template, request
from flask import redirect, flash, jsonify

import database_controller as db

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


@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def catalog():
    """ Displays HTML tempplate for catalog homepage """
    test_genres = ['rock', 'hip-hop', 'classical']
    test_items = ['foo', 'bar']
    return render_template('catalog.html',
                           genres=test_genres,
                           recent_items=test_items)


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
            flash('Added artist to database: %s' % message[1])

        obj = dict(artist_name=message[1],
                   spotify_id=spotify_id,
                   artist_url=url_for('artist', artist=message[1]))
        return json.dumps(obj)
    else:
        return render_template('artist_create.html')


@app.route('/artist/edit/<int:artist>/')
@app.route('/artist/edit/<artist>/')
def artist_edit(artist):
    """ Edit database entry of a specific artist """
    artist = dict(name='Radiohead',
                  url_name='radiohead',
                  emergence='1990',
                  genres=['Rock', 'Alternative'],
                  top_songs=['No Surprises', 'Reckoner', 'Fake Plastic Trees'])

    return render_template('artist_edit.html', artist=artist)


@app.route('/artist/delete/<int:artist>/')
@app.route('/artist/delete/<artist>/')
def artist_delete(artist):
    """ Delete an artist from the database """
    artist = dict(name='Radiohead',
                  url_name='radiohead',
                  emergence='1990',
                  genres=['Rock', 'Alternative'],
                  top_songs=['No Surprises', 'Reckoner', 'Fake Plastic Trees'])
    return render_template('artist_delete.html', artist=artist)


# Genre CRUD routes

@app.route('/genre/<int:genre>/')
@app.route('/genre/<genre>/')
def genre(genre):
    """ Displays all artists corresponding to a specific genre """
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
    genre = dict(name='Alternative',
                 emergence='1980')
    artists = [radiohead, seratones]
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
