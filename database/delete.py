from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

def database_object(session, obj):
    ''' When passed a single database object, obtained through
    .one() or .first(), deletes that object from database '''
    session.delete(obj)

def database_objects(session, *collections):
    ''' When passed a collection of database objects
    (i.e. obtained by querying .all()), deletes all contained objects '''
    for coll in collections:
        for obj in coll:
            session.delete(obj)

def artist_genre(session, artist_id, genre_id):
    ''' Delete an ArtistGenre row corresponding to a specified
    art_id and gen_id '''
    artist_genre = session.query(ArtistGenre).filter_by(
        artist=artist_id, genre=genre_id).first()
    session.delete(artist_genre)
