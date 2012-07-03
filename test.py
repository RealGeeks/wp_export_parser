# coding=utf-8
import os
import unittest
import datetime
from StringIO import StringIO
from wp_export_parser.autop import wpautop
from wp_export_parser.parse import parse_post, parse_comment, parse_category, WPParser
from wp_export_parser.extract_images import get_all_linked_images
from xml.etree.ElementTree import fromstring

def wp_export_fragment(text,annoying_version="1.2"):
    namespace_header = """<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/{v}/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/{v}/"
        >""".format(v=annoying_version)
    namespace_footer = "</rss>"
    return namespace_header + text + namespace_footer



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
        comment = fromstring(wp_export_fragment("""
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
        """))
        parsed_comment = parse_comment(comment)
        expected = {'comment_date': datetime.datetime(2009,3,18,19,28,23), 'comment_approved': True, 'comment_author_url': 'http://realestateapproval.info/to-rent-or-buy-that-is-the-question/', 'comment_author_IP': '74.54.206.242', 'comment_content': u'[...] given thought to what is written here, you still want to buy a home, by all means do so.\xa0 Employ a Realtor that is contractually obligated and morally committed to work in your best interest, take the time [...]', 'comment_author': 'To Rent or Buy, That is the Question | Real Estate Approval', 'comment_author_email': 'pinged'}
        self.assertEquals(parsed_comment,expected)


class TestParseCategory(unittest.TestCase):
    def test_parse_category(self):
        category = fromstring(wp_export_fragment("""<category domain="category" nicename="bank-of-america-idiotcies"><![CDATA[Bank of America Idiotcies]]></category>""")).getchildren()[0]
        parsed_category = parse_category(category)
        self.assertEquals(parsed_category,'Bank of America Idiotcies')

class TestParsePost(unittest.TestCase):
    """
		<content:encoded><![CDATA[<img class="size-medium wp-image-4642 alignleft" style="margin: 10px;" title="Somewhere Home Owners it's Time to Sell" src="http://www.example.com/somewheredwellings/wp-content/uploads//2012/05/129-300x200.jpg" alt="" width="300" height="200" />The news is out, the real estate market has changed. Why?  There are a variety of reasons: # MLS -   # # # #

<o:p><font face="Arial"> </font></o:p><font face="Arial">Call 541-389-4511 or see his web site to search the MLS - <strong><a href="http://www.bendoregonrealestateexpert.com/"><font color="#800080">Bend Oregon Real Estate</font></a></strong>.Â:w 

Each month we ar].]e seeing the "Days on Market" average drop. Currently it is less than 3 months.]]></content:encoded>
    """
    post_text = """
	<item>
		<title>Somewhere Real Estate Sellers, Your Time Has Come!</title>
		<link>http://www.example.com/somewheredwellings/sellers-market/4641/</link>
		<pubDate>Sun, 27 May 2012 17:15:14 +0000</pubDate>
		<dc:creator>Kristal Kraft Somewhere Realtor</dc:creator>
		<description></description>
		<wp:post_id>4641</wp:post_id>
		<wp:post_date>2012-05-27 10:15:14</wp:post_date>
		<wp:post_date_gmt>2012-05-27 17:15:14</wp:post_date_gmt>
		<wp:post_name>sellers-market</wp:post_name>
		<wp:status>publish</wp:status>
<content:encoded><![CDATA[
<p align="center"> <a href="http://www.bendoregonrealestateexpert.com/bend-real-estate-blog/wp-content/uploads/2009/11/bend-oregon-real-estate-market.jpg" title="bend-oregon-real-estate-market.jpg"><img src="http://www.bendoregonrealestateexpert.com/bend-real-estate-blog/wp-content/uploads/2009/11/bend-oregon-real-estate-market.jpg" alt="bend-oregon-real-estate-market.jpg" /></a></p>
There are not many times in a person's life time that an opportunity comes along like the present opportunity to buy real estate in Bend Oregon.  Interest rates are hovering around 5% and home prices are almost 50% less than they were two years ago.

All economic indicators and news is positive.  The recession is coming to an end.  To top that off the Federal government is offering a tax credit to first time home buyers of $8,000!  Anyone who has not owned a home in the last 3 years should have their head examined if they don't buy a home within the next few months.

I look for the market to turn around this coming Spring/Summer.  Once unemployment starts to fall you can look for interest rates and home prices to start inching up.  I currently have 172 prospective buyers receiving automatic e-mails through my web site.  10% of these buyers plan on buying within the next few months.  Some are waiting for their homes to sell in other parts of the nation.

The other 90 are sitting on the fence.  They are not sure whether to buy now or wait.  Right now they are waiting.  I think there will be some sort of news that will shock this real estate market back to full life.  That could be rising interest rates, rising prices, inflation, rising employment or a combination of any of these factors.  When the news hits this market will break loose!

There are going to be a lot of people who are going to be saying "We should have bought a home in the winter of 2009."  Once the market turns construction will start up again.  More contractors will be moving back to Bend.  More jobs will be created and more people will be moving to Bend.  Prices will start to rise again.

And to top all this most economist agree that we will be seeing a substantial amount of inflation in the future because of all the government stimulus money now being spent.  The bottom line is that there may not be a better opportunity to buy a home or investment property in Bend for many years to come.  Now is the time to buy!
<p style="margin: 0in 0in 0pt" class="MsoNormal"><font face="Arial">If you’re thinking about buying a home in <st1:city><st1:place>Bend</st1:place></st1:city> you should sign up for Jim’s free <strong><a href="http://www.bendoregonrealestateexpert.com/bend-oregon-real-estate-new-listings-notification.html"><font color="#800080">New Listing Notification Service</font></a></strong> or call or e-mail today.  Jim Johnson is a Certified Residential Specialist and has been selling quality homes in <st1:place><st1:city>Bend</st1:city> <st1:state>Oregon</st1:state></st1:place> since 1981. </font></p>

<o:p><font face="Arial"> </font></o:p><font face="Arial">Call 541-389-4511 or see his web site to search the MLS - <strong><a href="http://www.bendoregonrealestateexpert.com/"><font color="#800080">Bend Oregon Real Estate</font></a></strong>.  Jim is licensed by the State of Oregon as the Principal Broker for Bend Oregon Real Estate Expert.<span>  </span><strong><a href="mailto:jimj@bendcable.com"><font color="#1900ff">E-MAIL</font></a><o:p></o:p></strong></font>]]></content:encoded>
<excerpt:encoded><![CDATA[]]></excerpt:encoded>
	</item>
        """

    def test_parse_post(self):
        post = fromstring(wp_export_fragment(self.post_text))
        parsed_post = parse_post(post)
        self.assertEquals(parsed_post['title'],'Somewhere Real Estate Sellers, Your Time Has Come!')
        assert('Real Estate Expert' in parsed_post['body'])

    def test_that_we_can_read_different_export_versions(self):
        post = fromstring(wp_export_fragment(self.post_text,annoying_version='1.0'))
        parsed_post = parse_post(post)
        post2 = fromstring(wp_export_fragment(self.post_text,annoying_version='1.1'))
        parsed_post2 = parse_post(post)
        self.assertEquals(parsed_post,parsed_post2)

    def test_parse_post_datetime_converstion(self):
        post = fromstring(wp_export_fragment(self.post_text))
        parsed_post = parse_post(post)
        self.assertEquals(parsed_post['pubDate'],datetime.datetime(2012,5,27,17,15,14))
    
class TestExtractDomain(unittest.TestCase):
    channel_text = """
    <channel>
	    <link>http://www.example.com/somewhere-real-estate-blog</link>
    </channel>
    """

    def test_extract_domain(self):
        parser = WPParser(StringIO(wp_export_fragment(self.channel_text)))
        self.assertEquals(parser.get_domain(),'www.example.com')
        
class TestGetPosts(unittest.TestCase):
    channel_text = """
<item>
<wp:post_type>post</wp:post_type>
<title>Title 1</title>
</item>
<item>
<wp:post_type>page</wp:post_type>
<title>Title 2</title>
</item>
    """

    def test_get_items(self):
        parser = WPParser(StringIO(wp_export_fragment(self.channel_text)))
        self.assertEquals(len([x for x in parser.get_items()]),2)
    

if __name__ == '__main__':
    unittest.main()
