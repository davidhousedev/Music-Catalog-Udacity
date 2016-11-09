import urllib
import urllib2
import json
import pprint # remove for production
import datetime

from api_keys import GOOGLE_API_KEY

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

# Define maximum number of top songs that should be stored in database
TOP_SONG_LIMIT = 3

def db_add_artist(spotify_id):
    """ Queries Spotify by artist id for artist info and top tracks
    then adds artist to appropriate database tables """
    get_youtube_id('radiohead', 'reckoner')
    # Retrieve artist information from Spotify
    url = 'https://api.spotify.com/v1/artists/%s' % spotify_id
    data = json.load(urllib2.urlopen(url))
    print 'id is %s' % spotify_id
    print 'name is %s' % data[u'name'].lower()
    artist_name = data[u'name']
    artist_genres = data[u'genres']

    # Retrieve artist top songs from Spotify
    url += '/top-tracks/?country=US'
    song_data = json.load(urllib2.urlopen(url))
    artist_top_songs = []
    for track in song_data[u'tracks']:
        artist_top_songs.append(track[u'name'])
    # Obtain video IDs from youtube corresponding to top songs
    youtube_ids = []
    #global TOP_SONG_LIMIT
    for song in artist_top_songs:
        vid_id = get_youtube_id(artist_name, song)
        youtube_ids.append(vid_id)
        if len(youtube_ids) == TOP_SONG_LIMIT:
            break
    pprint.pprint(youtube_ids)

    new_artist = Artist(name=artist_name,
                        spotify_id=spotify_id,
                        url_name=artist_name.lower(),
                        created=datetime.datetime.utcnow())

    session = DBSession()
    try:
        session.add(new_artist)
        session.commit()
        # Retrieve new artist from DB, to use artist art_id
        artist_id = artist_by_spotify_id(session, spotify_id).art_id
        print 'Added artist: %s' % artist_id
        # Add any new genres to database
        update_genres(session, artist_genres)
        session.commit()
        # Retrieve up-to-date genres from database
        db_genres = get_genres(session)
        for genre in db_genres:
            print genre.name
        # Add artist genres to database
        update_artist_genres(session, artist_id, artist_genres)
        # Add artist top songs to database

        session.commit()
        artist_genres = session.query(ArtistGenre).all()
        print artist_genres

    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()

def artist_by_spotify_id(session, spotify_id):
    """ Queries database for artist and returns if found """
    spotify_id = unicode(spotify_id)
    try:
        artist = session.query(Artist).filter_by(spotify_id=spotify_id).one()
        return artist
    except Exception, e:
        raise e

def get_genres(session):
    return session.query(Genre).all()

def get_genre_by_name(session, name):
    ''' Searches database for a specific genre, by genre name.
    Returns a genre object corresponding to the name '''
    genre_name = unicode(name.lower())
    return session.query(Genre).filter_by(name=genre_name).one()

def update_genres(session, new_genres):
    ''' When passed a db session and a list of music genres,
    this function adds all new genres to database '''
    db_genres = get_genres(session)
    db_genre_names = []
    for genre in db_genres:
        db_genre_names.append(genre.name)
    for genre in new_genres:
        if genre not in db_genre_names:
            print 'trying to add %s' % genre
            new_genre = Genre(name=genre,
                              created=datetime.datetime.utcnow())
            session.add(new_genre)

def update_artist_genres(session, artist_id, genres):
    ''' When passed a db session, a db art_id, and a list of genre strings,
    updates the ArtistGenre table with a row linking the artist with a genre '''
    for genre in genres:
        genre_id = get_genre_by_name(session, genre).gen_id
        print 'adding: %s %s' % (artist_id, genre_id)
        new_artist_genre = ArtistGenre(artist=artist_id,
                                       genre=genre_id)
        session.add(new_artist_genre)

def get_youtube_id(artist, song_name):
    ''' Searches youtube videos for an artist and song name,
    and returns a youtube video ID as a unicode string '''
    global GOOGLE_API_KEY
    url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {'part': 'snippet',
               'q': '%s %s' % (artist, song_name),
               'key': GOOGLE_API_KEY}
    url += '?' + urllib.urlencode(headers)
    youtube_data = json.load(urllib2.urlopen(url))
    return youtube_data[u'items'][0][u'id'][u'videoId']