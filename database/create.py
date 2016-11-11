import datetime

from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

import database.get as get
from database.database_helpers import listify

def genres(session, new_genres):
    ''' When passed a db session and a list of music genres,
    this function adds all new genres to database '''
    db_genres = get.genres(session)
    db_genre_names = listify(db_genres, 'name')
    # Add genres that are not currently in database
    for genre in new_genres:
        if genre not in db_genre_names:
            new_genre = Genre(name=genre,
                              created=datetime.datetime.utcnow())
            session.add(new_genre)

def artist_genres(session, artist_id, genre_names):
    ''' When passed a db session, a db art_id, and a list of genre strings,
    updates the ArtistGenre table with a row linking the artist with a genre '''
    for genre in genre_names:
        genre_id = get.genre_by_name(session, genre).gen_id
        new_artist_genre = ArtistGenre(artist=artist_id,
                                       genre=genre_id)
        session.add(new_artist_genre)
