import re
import datetime
from urlparse import urlparse
from xml.etree.ElementTree import iterparse
from .autop import wpautop
from . import parse_shortcodes


def parse_pubdate(datestr):
    """
    Attempt to parse the weird date format that wordpress uses
    for its publication dates.  Strip out the strange -0001 year
    see every now and then and replace with 1970 because 1970 was
    a good year.
    """
    datestr = re.sub(r' \+0000$', '', datestr)
    datestr = re.sub(r'-0001', '1970', datestr)
    return datetime.datetime.strptime(datestr, '%a, %d %b %Y %H:%M:%S')


def parse_post(post):
    out = {}
    out['postmeta'] = {}
    for element in post.getiterator():
        if 'title' in element.tag:
            out['title'] = element.text
        elif 'post_name' in element.tag:
            out['post_name'] = element.text
        elif 'post_id' in element.tag:
            out['post_id'] = element.text
        elif 'post_type' in element.tag:
            out['post_type'] = element.text
        elif 'pubDate' in element.tag and element.text:
            out['pubDate'] = parse_pubdate(element.text)
        elif 'status' in element.tag:
            out['status'] = element.text
        elif 'link' in element.tag:
            out['link'] = element.text
        elif 'encoded' in element.tag and 'content' in element.tag:
            out['body'] = parse_shortcodes.parse(wpautop(element.text))
        elif 'postmeta' in element.tag:
            for meta_element in element.getchildren():
                if 'meta_key' in meta_element.tag:
                    key = meta_element.text
                elif 'meta_value' in meta_element.tag:
                    value = meta_element.text
            out['postmeta'][key] = value
    return out


def parse_comment(comment):
    out = {}
    for element in comment.getiterator():
        if 'comment_author_email' in element.tag:
            out['comment_author_email'] = element.text
        elif 'comment_author_IP' in element.tag:
            out['comment_author_IP'] = element.text
        elif 'comment_author_url' in element.tag:
            out['comment_author_url'] = element.text
        elif 'comment_author' in element.tag:
            out['comment_author'] = element.text
        elif 'comment_content' in element.tag:
            out['comment_content'] = element.text
        elif 'comment_date' in element.tag:
            out['comment_date'] = datetime.datetime.strptime(element.text, '%Y-%m-%d %H:%M:%S')
        elif 'comment_approved' in element.tag:
            out['comment_approved'] = bool(element.text)
    return out


def parse_category(category):
    return category.text


def get_comments(post):
    comments = post.findall('{http://wordpress.org/export/1.0/}comment')
    for c in comments:
        yield parse_comment(c)


def get_categories(post):
    categories = post.findall('category')
    for c in categories:
        if c.get('domain') == 'category':
            yield parse_category(c)


class WPParser(object):
    def __init__(self, input_file):
        self.input_file = input_file

    def get_domain(self):
        self.input_file.seek(0)
        for event, elem in iterparse(self.input_file):
            if elem.tag == 'channel':
                return urlparse(elem.find('./link').text).hostname

    def get_items(self):
        self.input_file.seek(0)
        for event, elem in iterparse(self.input_file):
            if elem.tag == 'item':
                out = parse_post(elem)
                out['comments'] = get_comments(elem)
                out['categories'] = get_categories(elem)
                yield out
                elem.clear()
