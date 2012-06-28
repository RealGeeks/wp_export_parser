from xml.etree.ElementTree import fromstring
from .autop import wpautop

def parse_post(post):
    out = {}
    for element in post.getiterator():
        if 'title' in element.tag:
            out['title'] = element.text
        if 'post_name' in element.tag:
            out['post_name'] = element.text
        if 'post_id' in element.tag:
            out['post_id'] = element.text
        if 'post_type' in element.tag:
            out['post_type'] = element.text
        if 'link' in element.tag:
            out['link'] = element.text
    out['body'] = wpautop(post.findtext('{http://purl.org/rss/1.0/modules/content/}encoded'))
    out['comments'] = get_comments(post)
    out['categories'] = get_categories(post)
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
            out['comment_date'] = element.text
        if 'comment_author_IP' in element.tag:
            out['comment_author_IP'] = element.text
    return out

def parse_category(category):
    return category.text

def get_posts(input_string):
    data = fromstring(input_string)
    posts = data.findall('.//item')
    for post in posts:
        yield parse_post(post)

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

