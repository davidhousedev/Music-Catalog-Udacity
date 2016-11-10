from urllib import unquote_plus

def parse_url(url):
    ''' Replaces URL escapes with native values,
    and converts to int if string is all nums) '''
    if type(url) != int:
        url = unquote_plus(url)
    return url