import re
from .shortcodes import youtube

TAGS_WE_CAN_PARSE = {
    'youtube':youtube,
}

def replace_tags(match):
    return youtube.parse(match)

def parse(post_body):
    """
    I stole this shortcode regex from Wordpress's source.  It is very confusing.
    """
    tagregexp = '|'.join([re.escape(t) for t in TAGS_WE_CAN_PARSE.keys()])
    pattern = re.compile('\\[(\\[?)(' + tagregexp + ')\\b([^\\]\\/]*(?:\\/(?!\\])[^\\]\\/]*)*?)(?:(\\/)\\]|\\](?:([^\\[]*(?:\\[(?!\\/\\2\\])[^\\[]*)*)\\[\\/\\2\\])?)(\\]?)')
    return re.sub(pattern,replace_tags,post_body)
