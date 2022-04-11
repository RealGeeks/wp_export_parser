try:
    from html import escape
except ImportError:
    from cgi import escape

def get_data(tag_atts, tag_contents):
    """
    From wordpress source: https://github.com/WordPress/WordPress/blob/master/wp-includes/media.php#L620
    return '<div ' . $id . 'class="wp-caption ' . esc_attr($align) . '" style="width: ' . (10 + (int) $width) . 'px">'
    . do_shortcode( $content ) . '<p class="wp-caption-text">' . $caption . '</p></div>';
    
    """
    if not tag_atts:
        return ''
    tag_atts = dict([(a[0], a[1]) for a in tag_atts])
    return u"<div id=\"{id}\" class='wp-caption' align=\"{align}\" style=\"width: '{width}px'\">{content}<p class='wp-caption-text'>{caption}</p></div>". format(
        id = escape(tag_atts.get('id',''), True),
        align = escape(tag_atts.get('align','alignnone'), True), 
        width = int(tag_atts.get('width',0)) + 10,
        content = tag_contents,
        caption = tag_atts.get('caption',''),
    )
