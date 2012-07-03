#wp_export_parser

[![Build Status](https://secure.travis-ci.org/RealGeeks/wp_export_parser.png?branch=master)](http://travis-ci.org/RealGeeks/wp_export_parser)

Parsing XML sucks.  This library provides a cleaner interface to get at the data in a [Wordpress](http://wordpress.org) export XML file.  

I'm using the built-in `etree.ElementTree` parser to parse the [Wordpress XML file](http://en.blog.wordpress.com/2006/06/12/xml-import-export/).

If you have a Wordpress export that breaks the parser I feel your pain.  Try looking at the line that Expat is barfing on and manually fixing it.

#Features

wp_export_parser can extract the following features from a Wordpress export file:

 * Posts
 * Pages
 * Comments
 * Categories


```python
from wp_export_parser import WPParser

with open('wp-export.xml') as export_file:
    parser = WPParser(export_file.read())
    print parser.get_domain() # outputs www.example.com
    for p in parser.get_post_and_pages():
        categories = p['categories']
        comments = p['comments']
        title = p['title']
        type = p['post_type'] #type can be 'page' or 'post'
```

#Notes
 * `wp_eport_parser` will parse files iteratively so it *should* be able to handle really large exports.  `get_pages()` returns a generator.
 * `wp_export_parser` sometimes will return unicode strings for the blog contents.
