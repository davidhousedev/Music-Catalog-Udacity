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


def artist_top_songs(session, songs_obj, artist_id):
    ''' For each song in songs_obj, updates corresponding
    artist top songs to reflect changes in songs_obj '''
    for song, data in songs_obj.iteritems():
        top_song = get.top_song(session, artist_id, song)
        if top_song.name != data['title'] or top_song.youtube_id != data['id']:
            top_song.name = data['title']
            top_song.youtube_id = data['id']
            session.add(top_song)


def genre(session, name, gen_id):
    ''' Updates a specific genre with a new name,
    and updates the genre's url_name to reflect changes '''
    genre = session.query(Genre).filter_by(gen_id=gen_id).one()
    genre.name = name
    genre.url_name = url_name(name)
    session.add(genre)


def artist_genres_by_genre(session, artist_ids, gen_id):
    ''' Updates artist relationships for a specific genre
    according to a list of artist_ids '''
    genre_name = get.genre_by_id(session, gen_id).name
    db_artist_objs = get.artists_by_genre(session, gen_id)
    db_artist_ids = listify(db_artist_objs, 'art_id')
    for art_id in artist_ids:
        if art_id not in db_artist_ids:
            create.artist_genre(session, art_id, genre_name)
    for art_id in db_artist_ids:
        if art_id not in artist_ids:
            delete.artist_genre(session, art_id, gen_id)


def influences(session, children, gen_id):
    ''' Updates a single genre's influence relationships
    to reflect a list of genre ids in param:children '''
    db_children_objs = session.query(Influence).filter_by(
        parent=gen_id).all()
    db_children_ids = listify(db_children_objs, 'child')
    for child in children:
        if child not in db_children_ids:
            create.influence(session, gen_id, child)
    for child in db_children_ids:
        if child not in children:
            delete.influence(session, gen_id, child)
