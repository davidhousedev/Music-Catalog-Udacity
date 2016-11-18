import datetime

from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

import database.get as get
from database.database_helpers import listify, api_spotify_top_tracks
from database.database_helpers import get_youtube_ids, TOP_SONG_LIMIT
from database.database_helpers import url_name


def artist(session, name, spotify_id):
    ''' When passed an artist name and spotify_id,
    creates an artist record in the database '''
    print 'test'
    encoded_name = url_name(name)
    print encoded_name
    new_artist = Artist(name=name,
                        spotify_id=spotify_id,
                        url_name=url_name(name),
                        created=datetime.datetime.utcnow())
    session.add(new_artist)

def genre(session, name):
    ''' Creates a new row in the Genre table '''
    new_genre = Genre(name=name,
                      url_name=url_name(name),
                      created=datetime.datetime.utcnow())
    session.add(new_genre)
    print 'returning %s' % new_genre.url_name
    return new_genre.url_name

def genres(session, new_genres):
    ''' When passed a db session and a list of music genres,
    this function adds all new genres to database '''
    db_genres = get.genres(session)
    db_genre_names = listify(db_genres, 'name')
    # Add genres that are not currently in database
    for gen_name in new_genres:
        if gen_name not in db_genre_names:
            genre(session, gen_name)

def artist_genre(session, artist_id, genre_name):
    ''' Creates a single artist genre in the database '''
    genre_id = get.genre_by_name(session, genre_name).gen_id
    new_artist_genre = ArtistGenre(artist=artist_id,
                                   genre=genre_id)
    session.add(new_artist_genre)

def artist_genres(session, artist_id, genre_names):
    ''' When passed a db session, a db art_id, and a list of genre strings,
    updates the ArtistGenre table with a row linking the artist with a genre '''
    for genre in genre_names:
        genre_id = get.genre_by_name(session, genre).gen_id
        new_artist_genre = ArtistGenre(artist=artist_id,
                                       genre=genre_id)
        session.add(new_artist_genre)

def top_songs(session, artist_name, spotify_id, artist_id):
    artist_top_songs = api_spotify_top_tracks(spotify_id)
    youtube_ids = get_youtube_ids(artist_name, artist_top_songs)
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

def influence(session, parent_id, child_id):
    ''' Creates an Influence row, linking the parent genre
    to the child genre by genre database id '''
    inf = Influence(parent=parent_id, child=child_id)
    session.add(inf)