import urllib
import urllib2
import json
from database_setup import Base, Artist
from api_keys import GOOGLE_API_KEY


def listify(objs, attr):
    ''' Returns a list of values of a specific database object attribute
    e.g. all names of database artists '''
    attr_list = []
    for obj in objs:
        attr_list.append(obj.serialize[attr])
    return attr_list


def listify_multi(objs, *attrs):
    ''' Iterates through database objs and returns a list of tuples
    with the values resulting from: obj.attr '''
    attr_list = []
    for obj in objs:
        song = []
        for attr in attrs:
            song.append(obj.serialize[attr])
        print song
        attr_list.append(tuple(song))
    return attr_list


def get_youtube_id(artist, song_name):
    ''' Searches youtube videos for an artist and song name,
    and returns a youtube video ID as a unicode string '''
    global GOOGLE_API_KEY
    url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {'part': 'snippet',
               'q': '%s %s' % (artist, song_name),
               'key': GOOGLE_API_KEY}
    url += '?' + urllib.urlencode(headers)
    youtube_data = json.load(urllib2.urlopen(url))
    return youtube_data[u'items'][0][u'id'][u'videoId']


def api_spotify_top_tracks(spotify_id):
    ''' Returns a descending ordered list of top track names
    for a specific spotify artist '''
    url = 'https://api.spotify.com/v1/artists/%s' % spotify_id
    url += '/top-tracks/?country=US'
    track_data = json.load(urllib2.urlopen(url))
    artist_top_track = []
    for track in track_data[u'tracks']:
        artist_top_track.append(track[u'name'])
    return artist_top_track
