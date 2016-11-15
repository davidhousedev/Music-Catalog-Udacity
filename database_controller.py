import urllib
import urllib2
import json
import pprint  # remove for production
import datetime

import database.get as get
import database.create as create
import database.update as update
import database.delete as delete
from database.database_helpers import listify, listify_multi, get_youtube_ids
from database.database_helpers import api_spotify_top_tracks, api_youtube_first_result
from database.database_helpers import api_spotify_artist, url_name

# Initializes python shell to interface with database
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

from database.database_helpers import TOP_SONG_LIMIT

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Establish database connection session
DBSession = sessionmaker(bind=engine)


def db_add_artist(spotify_id):
    """ Queries Spotify by artist id for artist info and top tracks
    then adds artist to appropriate database tables
    Returns tuple ('add', artist_name) if successful """

    session = DBSession()
    try:
        print 'line 38'
        artist_name, artist_genres = api_spotify_artist(spotify_id)
        print 'line 40'
        # Add artist record to database
        print artist_name, spotify_id
        create.artist(session, artist_name, spotify_id)
        print 'line 41'
        # Retrieve new artist from DB, to use artist art_id
        artist_id = get.artist_by_spotify_id(session, spotify_id).art_id
        # Add any new genres to database
        create.genres(session, artist_genres)
        print 'line 46'
        # Add artist genres to database
        create.artist_genres(session, artist_id, artist_genres)
        print 'line 48'
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
    ''' Retrieves an artist and related tables from database,
    and formats it for easy handling and display '''
    session = DBSession()
    db_artist = None
    try:
        if type(artist) is int:
            db_artist = get.artist_by_database_id(session, artist)
        else:
            db_artist = get.artist_by_url_name(session, artist)
        print 'artist url name is %s' % db_artist.url_name
        artist = dict(name=db_artist.name,
                      url_name=db_artist.url_name,
                      art_id=db_artist.art_id)
        if artist:
            genre_objs = get.genres_by_artist(session, artist['art_id'])
            artist['genres'] = listify(genre_objs, 'name')
            song_objs = get.top_songs_by_artist(session, artist['art_id'])
            artist['top_songs'] = listify_multi(
                song_objs, 'name', 'youtube_id')

    except Exception, e:
        raise e
    finally:
        session.close()

    return artist


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


def db_get_all_genres():
    ''' Returns a list containing genre names '''
    session = DBSession()
    try:
        genres = get.genres(session)
        genre_names = listify(genres, 'name')
    except Exception, e:
        raise e
    finally:
        session.close()

    return genre_names


def db_get_recent_additions(num):
    ''' Returns a list of recently added artists num entries long '''
    session = DBSession()
    try:
        artists = get.artists(session, num)
        artist_names = listify(artists, 'name')
    except Exception, e:
        raise e
    finally:
        session.close()

    return artist_names
