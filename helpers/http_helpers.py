from urllib import unquote
from database.database_helpers import url_name

def parse_url(url):
    ''' Replaces URL escapes with native values,
    and converts to int if string is all nums) '''
    if type(url) != int:
        url = unquote(url)
    return url

def parse_edit_form_data(form_data):
    ''' Parses form data from artist edit form
    and returns a dictionary organized by information type '''
    data = dict(name='',
                genres=[],
                top_songs={})
    for key, value in form_data.iteritems():
        key = key.rsplit('|')
        if key[0] == r'name':
            data['name'] = value
            continue
        if key[0] == r'genre':
            data['genres'].append(key[1])
            continue
        # Organize songs by numerical ranking in data dictionary
        if key[0] == r'song':
            key[2] = int(key[2]) + 1
            print key[0], key[1], key[2]
            if key[2] not in data['top_songs']:
                data['top_songs'][key[2]] = {}
            data['top_songs'][key[2]][key[1]] = value
            continue
    return data

def parse_genre_form_data(form_data):
    ''' Parses form data derived from a genre creation or edit,
    and returns a dictionary with the form data organized by data type '''
    genre = dict(name=None,
                 influences=[],
                 artists=[])
    for item in form_data:
        if item == 'name':
            genre['name'] = form_data['name']
        else:
            item_split = item.split('|')
            if item_split[0] == 'artist':
                genre['artists'].append(int(item_split[1]))
            else:
                genre['influences'].append(int(item_split[1]))
    return genre

