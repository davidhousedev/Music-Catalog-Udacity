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


def genre_by_id(session, id):
    ''' Searches database for a specific genre, by gen_id.
    Returns a genre object corresponding to that id '''
    return session.query(Genre).filter_by(gen_id=int(id)).one()


def artists(session, limit=None):
    artists = session.query(Artist).order_by(desc(Artist.created)).limit(limit)
    return artists


def artist_by_database_id(session, art_id):
    ''' Queries database for artist and returns if found '''
    return session.query(Artist).filter_by(art_id=art_id).one()


def artist_by_spotify_id(session, spotify_id):
    ''' Queries database for artist and returns if found '''
    return session.query(Artist).filter_by(spotify_id=spotify_id).one()


def top_songs_by_artist(session, artist_id):
    ''' Retrieve all top songs from database filtered by art_id,
    and returns a list of database objects, ordered by rank '''
    return session.query(TopSongs).filter_by(
        artist=artist_id).order_by(TopSongs.rank).all()