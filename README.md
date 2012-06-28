#wp_export_parser

[![Build Status](https://secure.travis-ci.org/RealGeeks/wp_export_parser.png?branch=master)](http://travis-ci.org/RealGeeks/wp_export_parser)

Parsing XML sucks.  This library provides a cleaner interface to get at the data in a Wordpress export XML file.  

I'm using the built-in `etree.ElementTree` parser to parse the actual Wordpress XML file, and [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) to extract images from the body of the posts.

If you have a Wordpress export that breaks the parser (I *know* they are out there) send it over and I'll see what I can do to make it work.

#Features

wp_export_parser can extract the following features from a Wordpress export file:

 * Posts
 * Pages
 * Comments
 * Categories
 * Images linked in posts and pages


```python
from wp_export_parser import get_posts

with open('wp-export.xml') as export_file:
    for p in get_posts(export_file.read()):
        categories = p['categories']
        comments = p['comments']
        title = p['title']
        type = p['post_type'] #type can be 'page' or 'post'
```
