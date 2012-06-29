# coding=utf-8
import os
import unittest
import datetime
from wp_export_parser.autop import wpautop
from wp_export_parser.parse import parse_post, parse_comment, parse_category
from wp_export_parser.extract_images import get_all_linked_images
from xml.etree.ElementTree import fromstring

def wp_export_fragment(text,annoying_version='1.2'):
    namespace_header = """<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/{v}/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/{v}/"
        >""".format(v=annoying_version)
    namespace_footer = "</rss>"

    return fromstring(namespace_header + text + namespace_footer)


class TestAutop(unittest.TestCase):
    """
    I'm not really sure what all this autop function is supposed to do, so this
    tests some basic functionality I was able to divine from looking at it quickly.
    """
    def test_that_autop_inserts_p_tags(self):
        out = wpautop("br here\nand P here\n\ndid it work?")
        expected = "<p>br here<br />\nand P here</p>\n<p>did it work?</p>\n"
        self.assertEquals(out,expected)

    def test_that_autop_doesnt_add_p_in_the_middle_of_object_tags(self):
        out = wpautop("<object>\n\ntest\n\n</object>")
        expected = "<p><object>test</object></p>\n"
        self.assertEquals(out,expected)


class TestParseComment(unittest.TestCase):
    def test_parse_comment(self):
        comment = wp_export_fragment("""
		<wp:comment>
			<wp:comment_id>695</wp:comment_id>
			<wp:comment_author><![CDATA[To Rent or Buy, That is the Question | Real Estate Approval]]></wp:comment_author>
			<wp:comment_author_email>pinged</wp:comment_author_email>
			<wp:comment_author_url>http://realestateapproval.info/to-rent-or-buy-that-is-the-question/</wp:comment_author_url>
			<wp:comment_author_IP>74.54.206.242</wp:comment_author_IP>
			<wp:comment_date>2009-03-18 11:28:23</wp:comment_date>
			<wp:comment_date_gmt>2009-03-18 19:28:23</wp:comment_date_gmt>
			<wp:comment_content><![CDATA[[...] given thought to what is written here, you still want to buy a home, by all means do so.  Employ a Realtor that is contractually obligated and morally committed to work in your best interest, take the time [...]]]></wp:comment_content>
			<wp:comment_approved>1</wp:comment_approved>
			<wp:comment_type>pingback</wp:comment_type>
			<wp:comment_parent>0</wp:comment_parent>
			<wp:comment_user_id>0</wp:comment_user_id>
		</wp:comment>
        """)
        parsed_comment = parse_comment(comment)
        expected = {'comment_date': datetime.datetime(2009,3,18,19,28,23), 'comment_approved': True, 'comment_author_url': 'http://realestateapproval.info/to-rent-or-buy-that-is-the-question/', 'comment_author_IP': '74.54.206.242', 'comment_content': u'[...] given thought to what is written here, you still want to buy a home, by all means do so.\xa0 Employ a Realtor that is contractually obligated and morally committed to work in your best interest, take the time [...]', 'comment_author': '74.54.206.242', 'comment_author_email': 'pinged'}
        self.assertEquals(parsed_comment,expected)


class TestParseCategory(unittest.TestCase):
    def test_parse_category(self):
        category = wp_export_fragment("""<category domain="category" nicename="bank-of-america-idiotcies"><![CDATA[Bank of America Idiotcies]]></category>""").getchildren()[0]
        parsed_category = parse_category(category)
        self.assertEquals(parsed_category,'Bank of America Idiotcies')

class TestParsePost(unittest.TestCase):
    post_text = """
	<item>
		<title>Somewhere Real Estate Sellers, Your Time Has Come!</title>
		<link>http://www.example.com/somewheredwellings/sellers-market/4641/</link>
		<pubDate>Sun, 27 May 2012 17:15:14 +0000</pubDate>
		<dc:creator>Kristal Kraft Somewhere Realtor</dc:creator>
		<guid isPermaLink="false">http://www.example.com/somewheredwellings/?p=4641</guid>
		<description></description>
		<content:encoded><![CDATA[<img class="size-medium wp-image-4642 alignleft" style="margin: 10px;" title="Somewhere Home Owners it's Time to Sell" src="http://www.example.com/somewheredwellings/wp-content/uploads//2012/05/129-300x200.jpg" alt="" width="300" height="200" />The news is out, the real estate market has changed. Why?  There are a variety of reasons:
<ul>
	<li>Housing Inventory is low, very low.</li>
	<li>Interest rates are low, very low.</li>
	<li>Buyers are confident, they want to buy.</li>
</ul>
Last month in April the Somewhere Real Estate sales exceeded the amount of properties that were put on the market by 71 units.

The average sales price has increased $14,690 from March to $298,712.  That is a $26,800 increase from a year ago.

Metro Somewhere has become a HOT seller's market.  If you are a seller this is good  news.

If you are a buyer, it's not going to get any better.  Prices and eventually interest rates are going to rise.  When prices and/or interest rates increase, home affordability is lessened. This means you get less of a house, while paying more.

There is no better time to buy than now. Really.

Each month we are seeing the "Days on Market" average drop. Currently it is less than 3 months.]]></content:encoded>
		<excerpt:encoded><![CDATA[]]></excerpt:encoded>
		<wp:post_id>4641</wp:post_id>
		<wp:post_date>2012-05-27 10:15:14</wp:post_date>
		<wp:post_date_gmt>2012-05-27 17:15:14</wp:post_date_gmt>
		<wp:comment_status>open</wp:comment_status>
		<wp:ping_status>open</wp:ping_status>
		<wp:post_name>sellers-market</wp:post_name>
		<wp:status>publish</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>post</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="selling-your-home"><![CDATA[Selling Your Home]]></category>
		<wp:postmeta>
			<wp:meta_key>_edit_last</wp:meta_key>
			<wp:meta_value><![CDATA[3]]></wp:meta_value>
		</wp:postmeta>
	</item>
        """

    def test_parse_post(self):
        post = wp_export_fragment(self.post_text)
        parsed_post = parse_post(post)
        self.assertEquals(parsed_post['title'],'Somewhere Real Estate Sellers, Your Time Has Come!')
        assert('HOT seller\'s market' in parsed_post['body'])

    def test_that_we_can_read_different_export_versions(self):
        post = wp_export_fragment(self.post_text,annoying_version='1.0')
        parsed_post = parse_post(post)
        post2 = wp_export_fragment(self.post_text,annoying_version='1.1')
        parsed_post2 = parse_post(post)
        self.assertEquals(parsed_post,parsed_post2)

    def test_parse_post_datetime_converstion(self):
        post = wp_export_fragment(self.post_text)
        parsed_post = parse_post(post)
        self.assertEquals(parsed_post['pubDate'],datetime.datetime(2012,5,27,17,15,14))
    

class TestExtractImages(unittest.TestCase):
    def test_extract_images(self):
        test_html = """bleh bleh <br>dalihdaf</br><b><b><B>this html SUCKS<img src='http://www.poop.com/test/img.png' style="crap" align="INTERNET EXPLORDER!">"""
        self.assertEquals([u'http://www.poop.com/test/img.png'],get_all_linked_images(test_html))
        
    

if __name__ == '__main__':
    unittest.main()
