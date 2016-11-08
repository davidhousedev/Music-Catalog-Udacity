import urllib2
import json
import pprint # remove for production
import datetime

# Initializes python shell to interface with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artist, ArtistGenre, Genre
from database_setup import Influence, TopSongs

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Establish database connection session
DBSession = sessionmaker(bind=engine)

def db_add_artist(spotify_id):
    """ Queries Spotify by artist id for artist info and top tracks
    then adds artist to appropriate database tables """
    url = 'https://api.spotify.com/v1/artists/%s' % spotify_id
    data = json.load(urllib2.urlopen(url))
    pprint.pprint(data)
    print 'name is %s' % data[u'name'].lower()

    artist_name = data[u'name']
    new_artist = Artist(name=artist_name,
                        spotify_id=spotify_id,
                        url_name=artist_name.lower(),
                        created=datetime.datetime.utcnow())

    session = DBSession()
    try:
        session.add(new_artist)
        session.commit()
        artist = artist_by_spotify_id(session, spotify_id)
        print 'Added artist: %s' % artist.name
    except Exception, e:
        session.rollback()
        raise e

def artist_by_spotify_id(session, spotify_id):
    """ Queries database for artist and returns if found """
    spotify_id = unicode(spotify_id)
    try:
        artist = session.query(Artist).filter_by(spotify_id=spotify_id).one()
        return artist
    except Exception, e:
        raise e