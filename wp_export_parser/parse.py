import datetime
from urlparse import urlparse
from xml.etree.ElementTree import fromstring
from .autop import wpautop
from .extract_images import get_all_linked_images

def parse_post(post):
    out = {}
    for element in post.getiterator():
        if 'title' in element.tag:
            out['title'] = element.text
        elif 'post_name' in element.tag:
            out['post_name'] = element.text
        elif 'post_id' in element.tag:
            out['post_id'] = element.text
        elif 'post_type' in element.tag:
            out['post_type'] = element.text
        elif 'pubDate' in element.tag:
            out['pubDate'] = datetime.datetime.strptime(element.text,'%a, %d %b %Y %H:%M:%S +0000')
        elif 'status' in element.tag:
            out['status'] = element.text
        elif 'link' in element.tag:
            out['link'] = element.text
    out['body'] = wpautop(post.findtext('.//{http://purl.org/rss/1.0/modules/content/}encoded'))
    return out

def parse_comment(comment):
    out = {}
    for element in comment.getiterator():
        if 'comment_author' in element.tag:
            out['comment_author'] = element.text
        if 'comment_author_email' in element.tag:
            out['comment_author_email'] = element.text
        if 'comment_author_url' in element.tag:
            out['comment_author_url'] = element.text
        if 'comment_content' in element.tag:
            out['comment_content'] = element.text
        if 'comment_date' in element.tag:
            out['comment_date'] = datetime.datetime.strptime(element.text,'%Y-%m-%d %H:%M:%S')
        if 'comment_author_IP' in element.tag:
            out['comment_author_IP'] = element.text
    return out

def parse_category(category):
    return category.text

def get_comments(post):
    comments = post.findall('categories')
    if not comments:
        # Stupid namespace changed at some point, check for this one too
        comments = post.findall('{http://wordpress.org/export/1.0/}comment')
    for c in comments:
        yield parse_comment(c)
        
def get_categories(post):
    categories = post.findall('category')
    for c in categories:
        if c.get('domain') == 'category':
            yield parse_category(c)

            
class WPParser(object):
    def __init__(self,input_string):
        self.input_string = input_string
        self.data = fromstring(self.input_string)
        self.queued_images = set()
    
    def get_domain(self):
        return urlparse(self.data.find('.//channel/link').text).hostname

    def get_posts(self,extract_images=True):
        posts = self.data.findall('.//item')
        for post in posts:
            post = parse_post(post)
            post['comments'] = get_comments(post)
            post['categories'] = get_categories(post)
            if extract_images:
                images = get_all_linked_images(post['body'],ignore_unless=self.get_domain())
                if images:
                    self.queued_images.update(set(images))
            yield post

