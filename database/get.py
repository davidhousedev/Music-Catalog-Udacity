from sqlalchemy import desc
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs


def genres(session):
    return session.query(Genre).order_by(Genre.name).all()


def genre_by_name(session, name):
    ''' Searches database for a specific genre, by genre name.
    Returns a genre object corresponding to the name '''
    genre_name = name.lower()
    return session.query(Genre).filter_by(name=genre_name).one()

def genre_by_url_name(session, url_name):
    ''' Searches database for a specific genre, by genre.url_name.
    Returns a genre object corresponding to the name '''
    return session.query(Genre).filter_by(url_name=url_name).one()

def genre_by_id(session, id):
    ''' Searches database for a specific genre, by gen_id.
    Returns a genre object corresponding to that id '''
    return session.query(Genre).filter_by(gen_id=int(id)).one()


def genres_by_artist(session, artist_id):
    ''' Returns a list of all genre objects
    corresponding to a specific artist '''
    genre_objs = session.query(ArtistGenre).filter_by(artist=artist_id).all()
    genres = []
    for obj in genre_objs:
        genre = session.query(Genre).filter_by(gen_id=obj.genre).one()
        genres.append(genre)
    return genres


def artists(session, limit=None):
    artists = session.query(Artist).order_by(desc(Artist.created)).limit(limit)
    return artists


def artist_by_url_name(session, url_name):
    ''' Queries database for an artist by their url_name
    and returns an artist object if found '''
    return session.query(Artist).filter_by(url_name=url_name).one()


def artist_by_database_id(session, art_id):
    ''' Queries database for artist and returns if found '''
    return session.query(Artist).filter_by(art_id=art_id).one()


def artist_by_spotify_id(session, spotify_id):
    ''' Queries database for artist and returns if found '''
    return session.query(Artist).filter_by(spotify_id=spotify_id).one()


def artists_by_genre(session, genre_id):
    ''' Returns a list of all artist objects corresponding
    to a specific genre_id '''
    artist_genres = session.query(ArtistGenre).filter_by(genre=genre_id).all()
    artist_objs = []
    print 'line 60'
    for artist_genre in artist_genres:
        print artist_genre.artist
        artist = session.query(Artist).filter_by(
            art_id=artist_genre.artist).one()
        artist_objs.append(artist)
    return sorted(artist_objs, key=__index_to_name)



def top_song(session, artist_id, rank):
    print 'looking up: artist-%s, rank-%s' % (artist_id, rank)
    return session.query(TopSongs).filter_by(artist=artist_id, rank=rank).one()


def top_songs_by_artist(session, artist_id):
    ''' Retrieve all top songs from database filtered by art_id,
    and returns a list of database objects, ordered by rank '''
    return session.query(TopSongs).filter_by(
        artist=artist_id).order_by(TopSongs.rank).all()

def artist_genres_by_artist(session, artist_id):
    ''' Retrieves all ArtistGenre rows corresponding
    to a specific artist '''
    return session.query(ArtistGenre).filter_by(
        artist=artist_id).all()


def influences_by_genre_id(session, genre_id):
    ''' Returns a list of genre objects that are all influenced
    by the parameter: genre_id '''
    influence_objs = session.query(Influence).filter_by(parent=genre_id).all()
    genres = []
    for inf in influence_objs:
        gen = session.query(Genre).filter_by(gen_id=inf.child).one()
        genres.append(gen)
    return sorted(genres, key=__index_to_name)

# Helpers

def __index_to_name(db_obj):
    ''' Returns the name attribute of a database object
    Used for sorting objects in alphabetical order by name '''
    return db_obj.name