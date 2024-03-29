# wp_export_parser

[![Build Status](https://secure.travis-ci.org/RealGeeks/wp_export_parser.png?branch=master)](http://travis-ci.org/RealGeeks/wp_export_parser)

Parsing XML sucks.  This library provides a cleaner interface to get at the data in a [Wordpress](http://wordpress.org) export XML file.  

I'm using the built-in `etree.ElementTree` parser to parse the [Wordpress XML file](http://en.blog.wordpress.com/2006/06/12/xml-import-export/).

If you have a Wordpress export that breaks the parser I feel your pain.  Try looking at the line that Expat is barfing on and manually fixing it.

## Example Usage

```python
from wp_export_parser import WPParser

with open('wp-export.xml') as export_file:
    parser = WPParser(export_file)
    print parser.get_domain() # outputs www.example.com
    for p in parser.get_items():
        categories = p['categories']
        comments = p['comments']
        post_title = p['title']
        post_type = p['post_type']
        post_body = p['body']
        print "post type: {}\nPost title: {}\nPost : {}\n".format(post_type,
                                                                  post_title,
                                                                  post_body)
```

## Features

`wp_export_parser` can extract the following features from a Wordpress export file:

 * Posts
 * Pages
 * Comments (exposed as a generator returning dicts)
 * Categories (exposed as list of strings)
 * Postmeta (exposed as dict)

## Shortcodes
Wordpress export files often include *shortcodes*, which the Wordpress rendering engine replaces with HTML.  Since you probably aren't going to want to reimplement Wordpress's shortcodes in your own blogging engine, I have ripped out the shortcode parsing regular expressions and provided implementations of the most commonly-used shortcodes inside `wp_export_parser`.

 * `[youtube]`: `wp_export_parser` retrieves the correct embed code (using oEmbed) and replaces the shortcode transparently.
 * `[caption]`: `wp_export_parser` attempts to generate the same HTML Wordpress will generate (and assumes UTF-8 encoding)

Feel free to fork and contribute more shortcode support with a pull request

## Wordpress oddities
 * `wp_export_parser` attempts to emulate the same behavior Wordpress uses to add `<p>` and `<br>` tags.  I did this by attempting a 1-to-1 translation of the giant regular expression Wordpress uses to render posts.

## Notes
 * `wp_eport_parser` will parse files iteratively so it *should* be able to handle really large exports.  `get_pages()` returns a generator.
 * `wp_export_parser` sometimes will return unicode strings for the blog contents.
 * Tested with CPython 2.7 and 3.5

## To run the tests in docker
```
# Spin up docker container
docker build -t wp_export . && docker run -ti -v `pwd`:/opt/wp_export_parser wp_export bash
# From within the running container, run the tests
tox
```

## Changelog
* Added Dockerfile for Test environment
* Conditionally importing to support python 2.7 and 3.5
## License

Copyright (c) 2012-2022 Kevin McCarthy. Released under the terms of the MIT license.
