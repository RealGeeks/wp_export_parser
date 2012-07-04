import json
import httplib
import urllib2

def get_embed_code(video_id, width=800, height=600):
    """
    Do ghetto oembed call
    """
    url = 'http://www.youtube.com/oembed?url=http%3A//youtube.com/watch%3Fv%3D{video_id}&format=json&maxwidth={maxwidth}&maxheight={maxheight}'.format(
        video_id = video_id,
        maxwidth = width,
        maxheight = height,
    )
    try:
        resp =  json.loads(urllib2.urlopen(url).read())
        return resp['html']
    except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException):
        return ''

def parse(args):
    args = [a for a in args.split(' ') if a]
    return get_embed_code(*args)
    

