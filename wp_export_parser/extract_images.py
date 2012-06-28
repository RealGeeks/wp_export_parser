from bs4 import BeautifulSoup

def get_all_linked_images(post_body,ignore_unless=''):
    soup = BeautifulSoup(post_body)
    return [i['src'] for i in soup.find_all('img') if ignore_unless in i['src']]
