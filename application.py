from flask import Flask, url_for, render_template, request
from flask import redirect, flash, jsonify

# Initializes python shell to interface with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Establish database connection session
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def catalog():
    """ Displays HTML tempplate for catalog homepage """
    return 'Hello, homepage'


@app.route('/artist/<int:artist_id>/')
def artist(artist_id):
    """ Displays artist page by artist database id """
    return 'Hello, artist %s' % artist_id

@app.route('/artist/create')
def artist_create():
    """ Renders and processess form for creating artists """
    return 'Creating an artist'

@app.route('/artist/edit/<int:artist_id>/')
def artist_edit(artist_id):
    """ Edit database entry of a specific artist """
    return 'Editing artist %s' % artist_id

@app.route('/artist/delete/<int:artist_id>/')
def artist_delete(artist_id):
    """ Delete an artist from the database """
    return 'Deleting artist %s' % artist_id

if __name__ == '__main__':
    app.secret_key = 'turtles'  # TODO: Change me for production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
