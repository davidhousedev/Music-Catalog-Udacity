from sqlalchemy import update
import database.create as create
import database.get as get
import database.delete as delete
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs
from database.database_helpers import url_name, listify

def artist(session, name, art_id):
    ''' Updates an Artist row on the database with a new name,
    and updates the artist's url_name to reflect changes '''
    print 'trying to update %s, id: %s' % (name, art_id)
    artist = session.query(Artist).filter_by(art_id=art_id).first()
    artist.name = name
    artist.url_name = url_name(name)
    session.add(artist)

def artist_genres(session, genre_names, artist_id):
    ''' Checkes a list of genre names against the genres currently
    associated with an artist. Alters ArtistGenre database rows to
    reflect the genre list supplied in genre_names '''
    db_artist_genres = get.genres_by_artist(session, artist_id)
    db_genre_names = listify(db_artist_genres, 'name')
    for genre in genre_names:  # Add any new genres to database
        if genre not in db_genre_names:
            create.artist_genre(session, artist_id, genre)
    for db_genre in db_artist_genres:  # Delete any existing genres
        if db_genre.name not in genre_names:
            delete.artist_genre(session, artist_id, db_genre.gen_id)
