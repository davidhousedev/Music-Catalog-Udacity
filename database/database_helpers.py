import urllib, urllib2, json
from database_setup import Base, Artist
from api_keys import GOOGLE_API_KEY

def listify(objs, attr):
    ''' Returns a list of values of a specific database object attribute
    e.g. all names of database artists '''
    attr_list = []
    for obj in objs:
        attr_list.append(obj.serialize[attr])
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