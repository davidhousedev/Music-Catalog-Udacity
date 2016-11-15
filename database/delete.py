from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

def artist_genre(session, artist_id, genre_id):
    ''' Delete an ArtistGenre row corresponding to a specified
    art_id and gen_id '''
    artist_genre = session.query(ArtistGenre).filter_by(
        artist=artist_id, genre=genre_id).first()
    session.delete(artist_genre)
