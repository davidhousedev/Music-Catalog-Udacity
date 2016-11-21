import random
import string
from helpers.http_helpers import parse_url, parse_edit_form_data
import json
import pprint
import httplib2
import requests

from flask import Flask, url_for, render_template, request
from flask import redirect, flash, jsonify, session, make_response

import database_controller as db
from database.database_helpers import url_name

from oauth2client import client, crypt
from api_keys import GOOGLE_CLIENT_ID

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
                           genes=genres,
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


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for char in xrange(32))
    session['state'] = state
    return render_template('loginv2.html', STATE=state)

@app.route('/gconnect',
           methods=['POST'])
def authenticate_user():
    # if request.form['state'] != session['state']:
    #     response = make_response(json.dumps('Invalid state parameter.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
    # id_token = request.form['token']
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    id_token = request.data
    try:
        flow = client.flow_from_clientsecrets('client_secrets.json', scope='')
        flow.redirect_uri = 'postmessage'
        credentials = flow.step2_exchange(id_token)
    except client.FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token in the session
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    flash('You are now logged in as %s' % session['username'])
    return redirect(url_for('catalog'))


@app.route('/gdisconnect')
def disconnect_user():
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps("Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset user's session
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
    else:
        response = make_response(json.dumps("Failed to disconnect user"), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    return redirect(url_for('catalog'))





if __name__ == '__main__':
    app.secret_key = 'turtles'  # TODO: Change me for production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
