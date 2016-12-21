import json
import urllib
import urllib2
import pprint
from unicodedata import normalize
from database_setup import Base, Artist
from api_keys import GOOGLE_API_KEY

# Define maximum number of top songs that should be stored in database
TOP_SONG_LIMIT = 3


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
        attr_list.append(tuple(song))
    return attr_list


def get_youtube_ids(artist_name, top_song_list):
    ''' Returns a list of video ids corresponding to the param: top_song_list.
    Video ids will be in the same order as the list of top songs '''
    youtube_ids = []
    for song in top_song_list:
        vid_id = api_youtube_first_result(artist_name, song)
        if vid_id == None:
            continue
        youtube_ids.append(vid_id)
        if len(youtube_ids) == TOP_SONG_LIMIT:
            break
    return youtube_ids


def api_youtube_first_result(artist, song_name):
    ''' Searches youtube videos for an artist and song name,
    and returns a youtube video ID as a unicode string '''
    global GOOGLE_API_KEY
    url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {'part': 'snippet',
               'q': '%s %s' % (artist, song_name),
               'key': GOOGLE_API_KEY}
    url += '?' + urllib.urlencode(headers)
    youtube_data = json.load(urllib2.urlopen(url))
    for item in youtube_data[u'items']:
        if item[u'id'][u'kind'] == u'youtube#video':
            return item[u'id'][u'videoId']
    return None


def api_spotify_artist(spotify_id):
    ''' Returns an artist name and genres in a tuple
    from a Spotify API call '''
    url = 'https://api.spotify.com/v1/artists/%s' % spotify_id
    data = json.load(urllib2.urlopen(url))
    return (data[u'name'], data[u'genres'], data[u'images'])


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


def url_name(name):
    ''' Converts an artist or genre name into a url-friendly string.
    Remove accent marks and replaces spaces with + '''
    name = normalize('NFKD', name).encode('ascii', 'ignore').lower()
    return urllib.quote_plus(name)
