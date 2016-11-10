import urllib
import urllib2
import json
import pprint  # remove for production
import datetime

from api_keys import GOOGLE_API_KEY

# Initializes python shell to interface with database
from sqlalchemy import create_engine, desc
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
    then adds artist to appropriate database tables
    Returns tuple ('add', artist_name) if successful """
    get_youtube_id('radiohead', 'reckoner')
    # Retrieve artist information from Spotify
    url = 'https://api.spotify.com/v1/artists/%s' % spotify_id
    data = json.load(urllib2.urlopen(url))

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
    for song in artist_top_songs:
        vid_id = get_youtube_id(artist_name, song)
        youtube_ids.append(vid_id)
        if len(youtube_ids) == TOP_SONG_LIMIT:
            break

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
        # Add any new genres to database
        update_genres(session, artist_genres)
        session.commit()
        # Retrieve up-to-date genres from database
        db_genres = get_genres(session)
        # Add artist genres to database
        update_artist_genres(session, artist_id, artist_genres)
        # Add artist top songs to database
        if len(artist_top_songs) > TOP_SONG_LIMIT:
            songs_len = TOP_SONG_LIMIT
        else:
            songs_len = len(artist_top_songs)
        for i in xrange(songs_len):
            new_top_song = TopSongs(artist=artist_id,
                                    rank=i + 1,
                                    name=artist_top_songs[i],
                                    youtube_id=youtube_ids[i])
            session.add(new_top_song)
        session.commit()

    except Exception, e:
        session.rollback()
        raise e
    finally:
        session.close()

    return ('add', artist_name.lower())


def db_get_artist(artist):
    ''' Retrieves an artist and related tables from database,
    and formats it for easy handling and display '''
    session = DBSession()
    db_artist = None
    try:
        if type(artist) is int:
            db_artist = session.query(Artist).filter_by(art_id=artist).one()
        else:
            db_artist = session.query(Artist).filter_by(url_name=artist).one()

        artist = dict(name=db_artist.name,
                      url_name=db_artist.url_name,
                      art_id=db_artist.art_id)
        if artist:
            artist['genres'] = get_artist_genres(session, artist['art_id'])
            artist['top_songs'] = get_artist_top_songs(
                session, artist['art_id'])

    except Exception, e:
        raise e
    finally:
        session.close()

    return artist


def db_get_all_genres():
    ''' Returns a list containing genre names '''
    session = DBSession()
    try:
        genres = get_genre_names(session)
    except Exception, e:
        raise e
    finally:
        session.close()

    return genres


def db_get_recent_additions(num):
    ''' Returns a list of recently added artists num entries long '''
    session = DBSession()
    try:
        additions = get_recently_added_artists(session, num)
    except Exception, e:
        raise e
    finally:
        session.close()

    return additions


def artist_by_spotify_id(session, spotify_id):
    """ Queries database for artist and returns if found """
    spotify_id = unicode(spotify_id)
    try:
        artist = session.query(Artist).filter_by(spotify_id=spotify_id).one()
        return artist
    except Exception, e:
        raise e


def get_recently_added_artists(session, num):
    ''' Returns a list of the first num recently added artists '''
    artists = session.query(Artist).order_by(desc(Artist.created)).limit(num)
    names = []
    for artist in artists:
        names.append(artist.name)
    return names


def get_artist_genres(session, artist_id):
    ''' Returns a list of all genre names
    corresponding to a specific artist '''
    genre_objs = session.query(ArtistGenre).filter_by(artist=artist_id).all()
    genre_names = []
    for obj in genre_objs:
        genre = session.query(Genre).filter_by(gen_id=obj.genre).one()
        genre_names.append(genre.name)
    return genre_names


def get_artist_top_songs(session, artist_id):
    ''' Returns a list of tuples containing artist top song
    names and youtube video ids '''
    song_objs = session.query(TopSongs).filter_by(
        artist=artist_id).order_by(TopSongs.rank).all()
    songs = []
    for obj in song_objs:
        songs.append((obj.name, obj.youtube_id))
    return songs


def get_genres(session):
    return session.query(Genre).order_by(Genre.name).all()


def get_genre_names(session):
    genres = get_genres(session)
    names = []
    for genre in genres:
        names.append(genre.name)
    return names


def get_genre_by_name(session, name):
    ''' Searches database for a specific genre, by genre name.
    Returns a genre object corresponding to the name '''
    genre_name = unicode(name.lower())
    return session.query(Genre).filter_by(name=genre_name).one()


def get_genre_by_id(session, id):
    ''' Searches database for a specific genre, by gen_id.
    Returns a genre object corresponding to that id '''
    return session.query(Genre).filter_by(gen_id=int(id)).one()


def update_genres(session, new_genres):
    ''' When passed a db session and a list of music genres,
    this function adds all new genres to database '''
    db_genres = get_genres(session)
    db_genre_names = []
    for genre in db_genres:
        db_genre_names.append(genre.name)
    for genre in new_genres:
        if genre not in db_genre_names:
            new_genre = Genre(name=genre,
                              created=datetime.datetime.utcnow())
            session.add(new_genre)


def update_artist_genres(session, artist_id, genres):
    ''' When passed a db session, a db art_id, and a list of genre strings,
    updates the ArtistGenre table with a row linking the artist with a genre '''
    for genre in genres:
        genre_id = get_genre_by_name(session, genre).gen_id
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
