
import random
import string
from helpers.http_helpers import parse_url, parse_edit_form_data
import json
import pprint
import httplib2
import requests

from helpers.http_helpers import parse_url, parse_edit_form_data
from helpers.http_helpers import parse_genre_form_data

from database_setup import ARTIST_IMAGE_WIDTH_LG, ARTIST_IMAGE_WIDTH_MD
from database_setup import ARTIST_IMAGE_WIDTH_SM, ARTIST_IMAGE_WIDTH_XS

from flask import Flask, url_for, render_template, request
from flask import redirect, flash, jsonify, make_response
from flask import session as login_session

import database_controller as db
from database.database_helpers import url_name, listify

from oauth2client import client, crypt
from api_keys import GOOGLE_CLIENT_ID, FLASK_SECRET


app = Flask(__name__)

# Define number of recent additions to display on catalog homepage
MAX_RECENT_ADDITIONS = 5


#
# Primary Views
#

@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def catalog():
    """ Displays HTML tempplate for catalog homepage """
    genres = db.db_get_all_genres()
    recent_items = db.db_get_recent_additions(MAX_RECENT_ADDITIONS)
    return render_template('catalog.html',
                           genres=genres,
                           recent_items=recent_items,
                           img_lg=ARTIST_IMAGE_WIDTH_LG,
                           img_md=ARTIST_IMAGE_WIDTH_MD,
                           img_sm=ARTIST_IMAGE_WIDTH_SM,
                           img_xs=ARTIST_IMAGE_WIDTH_XS,
                           cur_user=login_session)


@app.route('/user/<int:user>/')
def user(user):
    """ Displays all genres and artists created by a specific user """
    user_id = int(user)
    user = db.db_get_user(user_id)
    print user
    artists = db.db_get_artists_by_user(user_id)
    genres = db.db_get_genres_by_user(user_id)
    return render_template('user.html',
                           user=user,
                           artists=artists,
                           genres=genres,
                           cur_user=login_session)


#
# Artist CRUD Routes
#

@app.route('/artist/<int:artist>/')
@app.route('/artist/<artist>/')
def artist(artist):
    """ Displays artist page by artist database id """
    artist, genres, songs = db.db_get_artist(parse_url(artist))
    return render_template('artist.html',
                           artist=artist,
                           genres=genres,
                           songs=songs,
                           img_lg=ARTIST_IMAGE_WIDTH_LG,
                           img_md=ARTIST_IMAGE_WIDTH_MD,
                           img_sm=ARTIST_IMAGE_WIDTH_SM,
                           img_xs=ARTIST_IMAGE_WIDTH_XS,
                           cur_user=login_session)


@app.route('/artist/create/',
           methods=['GET', 'POST'])
def artist_create():
    """ Renders and processess form for creating artists """
    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))

    if request.method == 'POST':
        form_data = request.form
        for item in form_data:
            spotify_id = item  # Retrieve Spotify ID from form data
            break
        message = db.db_add_artist(spotify_id, login_session)
        if message[0] == 'add':
            artist = db.db_get_artist(message[1])[0]

        obj = dict(artist_name=artist.name,
                   spotify_id=spotify_id,
                   artist_url=url_for('artist', artist=artist.url_name))
        return json.dumps(obj)
    else:
        return render_template('artist_create.html', cur_user=login_session)


@app.route('/artist/edit/<int:artist>/',
           methods=['GET', 'POST'])
@app.route('/artist/edit/<artist>/',
           methods=['GET', 'POST'])
def artist_edit(artist):
    """ Edit database entry of a specific artist """
    artist, genres, songs = db.db_get_artist(parse_url(artist))

    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))
    if login_session['user_id'] != artist.user:
        flash("You cannot edit another user's artist")
        return redirect(url_for('artist', artist=artist['url_name']))

    if request.method == 'POST':
        form_data = parse_edit_form_data(request.form)
        db.db_update_artist(form_data, artist.art_id)
        flash('Successfully updated artist: %s' % artist.name)
        return redirect(url_for('artist', artist=artist.art_id))

    # Filter out any genres that are already associated with this artist
    db_genre_objs = db.db_get_all_genres()
    art_gen_names = listify(genres, 'name')
    db_genres = [
        genre for genre in db_genre_objs if genre.name not in art_gen_names]
    return render_template('artist_edit.html',
                           artist=artist,
                           artist_genres=genres,
                           db_genres=db_genres,
                           artist_songs=songs,
                           cur_user=login_session)


@app.route('/artist/delete/<int:artist>/',
           methods=['GET', 'POST'])
@app.route('/artist/delete/<artist>/',
           methods=['GET', 'POST'])
def artist_delete(artist):
    """ Delete an artist from the database """
    artist = db.db_get_artist(artist)[0]

    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))
    if login_session['user_id'] != artist.user:
        flash("You cannot delete another user's artist")
        return redirect(url_for('artist', artist=artist['url_name']))

    if request.method == 'POST':
        db.db_delete_artist(artist.art_id)
        flash('Deleted artist: %s' % artist.name)
        return redirect(url_for('catalog'))

    return render_template('artist_delete.html',
                           artist=artist,
                           cur_user=login_session)


#
# Genre CRUD routes
#

@app.route('/genre/<int:genre>/')
@app.route('/genre/<genre>/')
def genre(genre):
    """ Displays all artists corresponding to a specific genre """
    genre, artists, influences = db.db_get_genre(parse_url(genre))
    return render_template('genre.html',
                           genre=genre,
                           artists=artists,
                           influences=influences,
                           img_lg=ARTIST_IMAGE_WIDTH_LG,
                           img_md=ARTIST_IMAGE_WIDTH_MD,
                           img_sm=ARTIST_IMAGE_WIDTH_SM,
                           img_xs=ARTIST_IMAGE_WIDTH_XS,
                           cur_user=login_session)


@app.route('/genre/create/',
           methods=['GET', 'POST'])
def genre_create():
    """ Create a new genre in the database """
    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))

    artists = db.db_get_all_artists()
    genres = db.db_get_all_genres()
    if request.method == 'POST':
        form_data = parse_genre_form_data(request.form)

        if not form_data['name']:
            flash('Genre name cannot be blank')
            return redirect(url_for('genre_create'))

        genre_name = db.db_create_genre(form_data['name'],
                                        form_data['artists'],
                                        form_data['influences'],
                                        login_session)[1]
        return redirect(url_for('genre', genre=genre_name))

    return render_template('genre_create.html',
                           artists=artists,
                           genres=genres,
                           cur_user=login_session)


@app.route('/genre/edit/<int:genre>/',
           methods=['GET', 'POST'])
@app.route('/genre/edit/<genre>/',
           methods=['GET', 'POST'])
def genre_edit(genre):
    """ Edit a specific genre """
    db_genre, gen_artists, gen_influences = db.db_get_genre(parse_url(genre))
    display_genre = db_genre  # Hacked solution to a strange template display issue

    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))
    if login_session['user_id'] != db_genre.user:
        flash("You cannot edit another user's genre")
        return redirect(url_for('genre', genre=db_genre.url_name))

    if request.method == 'POST':
        form_data = parse_genre_form_data(request.form)
        db.db_edit_genre(form_data['name'],
                         form_data['artists'],
                         form_data['influences'],
                         db_genre.gen_id)
        flash('Successfully updated genre: %s' % db_genre.name)
        return redirect(url_for('genre', genre=db_genre.gen_id))

    # Filter out artists and genres that are alreay associated with this genre
    db_artist_objs = db.db_get_all_artists()
    gen_art_names = listify(gen_artists, 'name')
    db_artists = [
        art for art in db_artist_objs if art.name not in gen_art_names]

    db_genres = db.db_get_all_genres()
    # Remove the viewed genre from display
    for gen in db_genres:
        if gen.gen_id == db_genre.gen_id:
            print 'deleting %s' % gen.name
            db_genres.remove(gen)
            break
    gen_inf_names = listify(gen_influences, 'name')
    db_genres = [gen for gen in db_genres if gen.name not in gen_inf_names]


    return render_template('genre_edit.html',
                           genre=display_genre,
                           gen_artists=gen_artists,
                           gen_influences=gen_influences,
                           db_artists=db_artists,
                           db_genres=db_genres,
                           cur_user=login_session)


@app.route('/genre/delete/<int:genre>/',
           methods=['GET', 'POST'])
@app.route('/genre/delete/<genre>/',
           methods=['GET', 'POST'])
def genre_delete(genre):
    """ Delete a specific genre """
    genre = db.db_get_genre(parse_url(genre))[0]

    # Verify that the current user has permission to perform this action
    if 'user_id' not in login_session:
        flash('You must be logged in to do that')
        return redirect(url_for('show_login'))
    if login_session['user_id'] != genre.user:
        flash("You cannot delete another user's genre")
        return redirect(url_for('genre', genre=genre.url_name))

    if request.method == 'POST':
        db.db_delete_genre(genre.gen_id)
        flash('Deleted genre: %s' % genre.name)
        return redirect(url_for('catalog'))

    return render_template('genre_delete.html',
                           genre=genre,
                           cur_user=login_session)


#
# Authentication
#

@app.route('/login')
def show_login():
    ''' Display login page to user, with server-generated state token.
    State token is passed back to the server to prevent CSRF attacks

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for char in xrange(32))
    login_session['state'] = state
    return render_template('loginv2.html', STATE=state, cur_user=login_session)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    ''' When provided with an access token, retrieves user information from
    Facebook and stores extended-use access token in user session. If user
    does not currently exist in database, create a new user record.

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    # Ensure that user is logging in from the login screen
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Retrieve access token
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['fb_id'] = data['id']
    login_session['provider'] = 'facebook'

    # The token must be stored in the login_session in order to properly logout
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data['data']['url']

    # If user is not already in database, create account for that e-mail
    db_user = db.db_get_user(login_session['email'])
    if not db_user:
        db_user = db.db_create_user(login_session)
    print 'logging in with user ID %s, %s' % (db_user.user_id, db_user.email)
    login_session['user_id'] = db_user.user_id
    return redirect(url_for('catalog'))


@app.route('/gconnect', methods=['POST'])
def authenticate_user():
    ''' When provided with a Google ID token, retrieves an API access token from
    Google to allow server-side API calls on behalf of the user. If the user does not
    currently exist in the database, creates a new user record.

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    if request.args.get('state') != login_session['state']:
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
        response = make_response(
            json.dumps('Failed to upgrade authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token in the login_session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # If user is not already in database, create account for that e-mail
    db_user = db.db_get_user(login_session['email'])
    if not db_user:
        db_user = db.db_create_user(login_session)
    print 'logging in with user ID %s, %s' % (db_user.user_id, db_user.email)
    login_session['user_id'] = db_user.user_id
    return redirect(url_for('catalog'))


@app.route('/disconnect')
def disconnect_user():
    ''' Logs user out from their third-party login service, and clears
    the current login session.

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    if 'provider' in login_session:
        provider = login_session['provider']
        if provider == 'google':
            if gdisconnect():
                del login_session['gplus_id']
            else:
                response = make_response(
                    json.dumps("Failed to disconnect Google user."), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
        if provider == 'facebook':
            if fbdisconnect():
                del login_session['fb_id']
            else:
                response = make_response(
                    json.dumps("Failed to disconnect Facebook user."), 401)
                response.headers['Content-Type'] = 'application/json'
                return response

        # Reset user's login_session
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
    else:
        response = make_response(json.dumps("Failed to disconnect user"), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    flash('Successfully logged out')
    return redirect(url_for('catalog'))


def fbdisconnect():
    ''' Disconnects user's login session on this app from Facebook

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    facebook_id = login_session['fb_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]
    return "you have been logged out"


def gdisconnect():
    ''' Disconnects user's login session on this app from Google

    Source: This method was provided by the Authentication and Authorization course
    hosted on Udacity.com'''
    access_token = login_session.get('access_token')
    if access_token is None:
        return False
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        return True
    else:
        return False


#
# API Endpoints
#

@app.route('/artists/json/')
def json_artists():
    artists = db.db_get_all_artists()
    artists_arry = None
    # If database data exists, prepare it to be returned as JSON
    if artists:
        artists_arry = [artist.serialize for artist in artists]

    return jsonify(artists=artists_arry)


@app.route('/genres/json/')
def json_genres():
    genres = db.db_get_all_genres()
    genres_arry = None
    # If database data exists, prepare it to be returned as JSON
    if genres:
        genres_arry = [genre.serialize for genre in genres]

    return jsonify(genres=genres_arry)


@app.route('/genre/<int:genre>/json/')
@app.route('/genre/<genre>/json/')
def json_genre(genre):
    genre, artists, influences = db.db_get_genre(parse_url(genre))

    genre_dict = dict(genre=None, artists=None, influences=None)
    # If database data exists, prepare it to be returned as JSON
    if genre:
        genre_dict['genre'] = genre.serialize
    if artists:
        genre_dict['artists'] = [artist.serialize for artist in artists]
    if influences:
        genre_dict['influences'] = [inf.serialize for inf in influences]

    return jsonify(genre=genre_dict)


@app.route('/artist/<int:artist>/json/')
@app.route('/artist/<artist>/json/')
def json_artist(artist):
    artist, genres, songs = db.db_get_artist(parse_url(artist))

    artist_dict = dict(artist=None, genres=None, songs=None)
    # If database data exists, prepare it to be returned as JSON
    if artist:
        artist_dict['artist'] = artist.serialize
    if songs:
        artist_dict['songs'] = [song.serialize for song in songs]
    if genres:
        artist_dict['genres'] = [genre.serialize for genre in genres]

    return jsonify(artist=artist_dict)


@app.route('/user/<int:user>/json/')
def json_user(user):
    """ Displays all genres and artists created by a specific user """
    user_id = int(user)
    user = db.db_get_user(user_id)
    artists = db.db_get_artists_by_user(user_id)
    genres = db.db_get_genres_by_user(user_id)

    user_dict = dict(name=None, artists=None, genres=None)
    # If database data exists, prepare it to be returned as JSON
    if user:
        user_dict['name'] = user.name
    if artists:
        user_dict['artists'] = [artist.serialize for artist in artists]
    if genres:
        user_dict['genres'] = [genre.serialize for genre in genres]

    return jsonify(user=user_dict)


if __name__ == '__main__':
    app.secret_key = FLASK_SECRET
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
