from sqlalchemy import update
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

def artist(session, name, art_id):
    print 'trying to update %s, id: %s' % (name, art_id)
    artist = session.query(Artist).filter_by(art_id=art_id).first()
    artist.name = name
    session.add(artist)

def artist_genres(session):
    pass