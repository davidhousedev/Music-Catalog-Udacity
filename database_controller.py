import urllib
import urllib2
import json
import pprint  # remove for production
import datetime

import database.get as get
import database.create as create
import database.update as update
import database.delete as delete
from database.database_helpers import get_youtube_ids
from database.database_helpers import api_spotify_top_tracks, api_youtube_first_result
from database.database_helpers import api_spotify_artist, url_name

# Initializes python shell to interface with database
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs, User

from database.database_helpers import TOP_SONG_LIMIT

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Establish database connection session
DBSession = sessionmaker(bind=engine, expire_on_commit=False)


def db_create_user(login_session):
    ''' Creates a user in the database based on information
    stored in a user login session. Returns new user object '''
    session = DBSession()
    try:
        new_user = create.user(session,
                               login_session['username'],
                               login_session['email'],
                               login_session['picture'])
        session.commit()
        return new_user
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()


def db_get_user(user):
    ''' Returns a user object either by email address or by user_id '''
    session = DBSession()
    try:
        if type(user) is int:
            return get.user_by_id(session, user)
        else:
            return get.user_by_email(session, user)
    except:
        return None
    finally:
        session.close()


def db_add_artist(spotify_id, login_session):
    """ Queries Spotify by artist id for artist info and top tracks
    then adds artist to appropriate database tables
    Returns tuple ('add', artist_name) if successful """

    session = DBSession()
    try:
        artist_name, artist_genres, artist_images = api_spotify_artist(spotify_id)
        # Add artist record to database
        print artist_name, spotify_id
        pprint.pprint(login_session)
        create.artist(session,
                      artist_name,
                      spotify_id,
                      artist_images,
                      login_session['user_id'])
        # Retrieve new artist from DB, to use artist art_id
        artist_id = get.artist_by_spotify_id(session, spotify_id).art_id
        # Add any new genres to database
        create.genres(session, artist_genres, login_session['user_id'])
        # Add artist genres to database
        create.artist_genres(session, artist_id, artist_genres)
        # # Add artist top songs to database
        create.top_songs(session,
                         url_name(artist_name),
                         spotify_id,
                         artist_id)

        session.commit()

    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()

    return ('add', artist_id)


def db_get_artist(artist):
    ''' Returns a tuple containing an artist object,
    a list of associated genre objects,
    and a list of associated artist top song objects '''
    session = DBSession()
    db_artist = None
    try:
        if type(artist) is int:
            db_artist = get.artist_by_database_id(session, artist)
        else:
            db_artist = get.artist_by_url_name(session, artist)

        genre_objs = get.genres_by_artist(session, db_artist.art_id)
        for genre in genre_objs:
            genre.num_artists = len(genre.artists)
        song_objs = get.top_songs_by_artist(session, db_artist.art_id)
        return db_artist, genre_objs, song_objs

    except Exception, e:
        raise e
    finally:
        session.close()



def db_get_all_artists():
    ''' Returns a list of artist objects containing all artists
    in the database '''
    session = DBSession()
    try:
        artists = get.artists(session)
    except Exception, e:
        raise e
    finally:
        session.close()
    return artists


def db_get_artists_by_user(user_id):
    ''' Returns a list of artist objects created by a specific user '''
    session = DBSession()
    try:
        artists = get.artists_by_user_id(session, user_id)
        return artists
    except Exception, e:
        raise e
    finally:
        session.close()


def db_update_artist(form_data, artist_id):
    ''' Updates database entry for an artist, genres, and top_songs
    based on information supplied by user form data '''
    pprint.pprint(form_data)
    session = DBSession()
    try:
        update.artist(session,
                      form_data['name'],
                      artist_id)
        update.artist_genres(session,
                             form_data['genres'],
                             artist_id)
        update.artist_top_songs(session,
                                form_data['top_songs'],
                                artist_id)
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()

    return ('update', artist_id)


def db_delete_artist(artist_id):
    ''' Deletes an artist, and its related genre and
    top songs relationships from the database '''
    session = DBSession()
    try:
        artist = get.artist_by_database_id(session, artist_id)
        delete.database_object(session, artist)
        genres = get.artist_genres_by_artist(session, artist_id)
        songs = get.top_songs_by_artist(session, artist_id)
        delete.database_objects(session, genres, songs)
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()

    return ('delete', artist_id)


def db_get_genre(genre):
    ''' Returns a tuple containing a genre object,
    a list of all artist_ids corresponding to that genre,
    and a list of genres influenced by that genre '''
    session = DBSession()
    print 'trying to get genre: %s' % genre
    try:
        if type(genre) is int:
            db_genre = get.genre_by_id(session, genre)
        else:
            db_genre = get.genre_by_url_name(session, genre)
        artists = get.artists_by_genre(session, db_genre.gen_id)
        influences = get.influences_by_genre_id(session, db_genre.gen_id)
    except Exception, e:
        raise e
    finally:
        session.close()
    return (db_genre, artists, influences)


def db_get_all_genres():
    ''' Returns a list of genre objects for all genres '''
    session = DBSession()
    try:
        genres = get.genres(session)
        for genre in genres:
            genre.num_artists = len(genre.artists)
    except Exception, e:
        raise e
    finally:
        session.close()

    return genres


def db_get_genres_by_user(user_id):
    ''' Returns a list of genre objects created by a specific user id '''
    session = DBSession()
    try:
        genres = get.genres_by_user(session, user_id)
        for genre in genres:
            genre.num_artists = len(genre.artists)
        return genres
    except Exception, e:
        raise e
    finally:
        session.close()


def db_create_genre(name, artists, influences, login_session):
    session = DBSession()
    try:
        new_genre = create.genre(session, name, login_session['user_id'])
        for artist_id in artists:
            create.artist_genre(session, artist_id, name)
        new_genre_id = get.genre_by_url_name(session, new_genre).gen_id
        for genre_id in influences:
            create.influence(session, new_genre_id, genre_id)
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()
    return ('add', new_genre)


def db_edit_genre(name, artists, influences, genre_id):
    ''' Updates a specified genre's name, artist associations,
    and genre influence associations '''
    session = DBSession()
    try:
        print name, artists, influences, genre_id
        update.genre(session, name, genre_id)
        update.artist_genres_by_genre(session, artists, genre_id)
        update.influences(session, influences, genre_id)
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()


def db_delete_genre(genre_id):
    ''' Deletes a genre, and associated ArtistGenre and Influence
    rows from the database '''
    session = DBSession()
    try:
        genre = get.genre_by_id(session, genre_id)
        delete.database_object(session, genre)
        artist_genres = get.artist_genres_by_genre(session, genre_id)
        delete.database_objects(session, artist_genres)
        influences = get.influences_by_genre_id(session, genre_id)
        delete.database_objects(session, influences)
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()
    return ('delete', genre_id)


def db_get_recent_additions(num):
    ''' Returns a list of recently added artists num entries long '''
    session = DBSession()
    try:
        artists = get.artists(session, num)
    except Exception, e:
        raise e
    finally:
        session.close()

    return artists
