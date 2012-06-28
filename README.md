#wp_export_parser

Parsing XML sucks.  This library provides a cleaner interface to get at the data in a Wordpress export XML file


```
from wp_export_parser import get_posts

with open('wp-export.xml') as export_file:
    for p in get_posts(export_file.read()):
        categories = p['categories']
        comments = p['comments']
        title = p['title']
        type = p['post_type'] #type can be 'page' or 'post'
```
