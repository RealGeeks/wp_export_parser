import json
import httplib
import urllib2


def get_embed_code(video_id, width=800, height=600):
    """
    Do hacky oembed call
    """
    url = 'https://www.youtube.com/oembed?url=https%3A//youtube.com/watch%3Fv%3D{video_id}&format=json&maxwidth={maxwidth}&maxheight={maxheight}'.format(
        video_id=video_id,
        maxwidth=width,
        maxheight=height,
    )
    try:
        resp = json.loads(urllib2.urlopen(url).read())
        return resp['html']
    except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException):
        return ''


def get_data(tag_atts, tag_contents):
    if not tag_atts:
        return ''
    tag_atts = [a[7] for a in tag_atts] #don't ask me why; this is just the funky format we are getting back from that parse_att regexp
    return get_embed_code(*tag_atts)
