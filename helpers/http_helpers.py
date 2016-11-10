from urllib import unquote_plus

def parse_url(url):
    ''' Replaces URL escapes with native values,
    and converts to int if string is all nums) '''
    if type(url) != int:
        url = unquote_plus(url)
    return url

def parse_edit_form_data(form_data):
    ''' Parses form data from artist edit form
    and returns a dictionary organized by information type '''
    data = dict(name='',
                genres=[],
                top_songs={})
    for key, value in form_data.iteritems():
        print key, value
        print data
        key = key.rsplit('-')
        if key[0] == r'name':
            data['name'] = value
            continue
        if key[0] == r'genre':
            data['genres'].append(key[1])
            continue
        # Organize songs by numerical ranking in data dictionary
        if key[0] == r'song':
            print key[0], key[1], key[2]
            if key[2] not in data['top_songs']:
                data['top_songs'][key[2]] = {}
            data['top_songs'][key[2]][key[1]] = value
            continue
    return data
