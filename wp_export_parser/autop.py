import re

"""
This is an attempt at a 1-to-1 php-to-python translation of the wpautop function in wordpress.

I did not invent the variable names pee and tinkle.  Those are copied from the wordpress people.

"""

def wpautop(pee, br = 1):
    if pee.strip() == '':
            return ''
    pee = pee + "\n" # just to make things a little easier, pad the end
    pee = re.sub('<br />\s*<br />', "\n\n", pee)

    # Space things ut a little
    allblocks = '(?:table|thead|tfoot|caption|col|colgroup|tbody|tr|td|th|div|dl|dd|dt|ul|ol|li|pre|select|form|map|area|blockquote|address|math|style|input|p|h[1-6]|hr|fieldset|legend)'
    pee = re.sub('(<' + allblocks + '[^>]*>)', "\n$1", pee)
    pee = re.sub('(</' + allblocks + '>)', "$1\n\n", pee)
    # Cross-platform newlines
    pee = pee.replace("\r\n", "\n")
    pee = pee.replace("\r", "\n")

    if pee.find('<object') != -1:
        pee = re.sub('\s*<param([^>]*)>\s*', "<param$1>", pee) # no pee inside object/embed
        pee = re.sub('\s*</embed>\s*', '</embed>', pee)
    pee = re.sub("/\n\n+/", "\n\n", pee) # take care of duplicates

    # make paragraphs, including one at the end
    pees = re.split('\n\s*\n', pee)
    pee = ''
    for tinkle in pees:
        pee += '<p>' + tinkle.strip("\n") + "</p>\n"
    pee = re.sub('<p>\s*</p>', '', pee) # under certain strange conditions it could create a P of entirely whitespace
    pee = re.sub('<p>([^<]+)</(div|address|form)>', "<p>$1</p></$2>", pee)
    pee = re.sub('<p>\s*(</?' + allblocks + '[^>]*>)\s*</p>', "$1", pee) # don't pee all over a tag
    pee = re.sub("<p>(<li.+?)</p>", "$1", pee) # problem with nested lists
    pee = re.sub('<p><blockquote([^>]*)>', "<blockquote$1><p>", pee)
    pee = pee.replace('</blockquote></p>', '</p></blockquote>')
    pee = re.sub('<p>\s*(</?' + allblocks + '[^>]*>)', "$1", pee)
    pee = re.sub('(</?' + allblocks + '[^>]*>)\s*</p>', "$1", pee)
    if br:
        pee = re.sub('(?<!<br />)\s*\n', "<br />\n", pee) # optionally make line breaks
        pee = pee.replace('<WPPreserveNewline />', "\n")
    pee = re.sub('(</?' + allblocks + '[^>]*>)\s*<br />', "$1", pee)
    pee = re.sub('<br />(\s*</?(?:p|li|div|dl|dd|dt|th|pre|td|ul|ol)[^>]*>)', '$1', pee)
    if pee.find('<pre') != -1:
        pee = re.sub_callback('(<pre[^>]*>)(.*?)</pre>', 'clean_pre', pee )
    pee = re.sub( "\n</p>$", '</p>', pee )

    return pee
