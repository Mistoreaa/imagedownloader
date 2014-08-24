

import re


class WebSite():

    domain = None
    domain_re = re.compile('http[s]?://[w]{3}?.*?/')
    host = None

    # Pattern to look for the link tag.
    a_tag_pattern = re.compile('<[\s]*a[\s]*href[\s]*=.*?>')
    a_link_pattern = re.compile('href[\s]*="(.*?)"')
    img_tag_pattern = re.compile('<[\s]*img[\s]*src[\s]*=.*?>')
    img_link_pattern = re.compile('src[\s]*="(.*?)"')

    ignore_imgname_regexs = []
    img_format = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    def __init__(self, url=None):
        self.domain = None
        self.required_url = url
        self.is_logged = True

    def set_required_url(self, url):
        self.required_url = url
        if url is None:
            return
        domain = self.domain_re.search(url)
        if domain:
            self.domain = domain.group(0)

    def parse_html(self, html):
        raise Exception('Not Impremented.')

    def search_a_tag(self, html):
        if not html: return []
        # search tags
        a_tag_list = self.a_tag_pattern.findall(html)
         
        urls = []
        # search urls
        for a_tag in a_tag_list:
            a_url_match = self.a_link_pattern.search(a_tag)
            if a_url_match:
                a_url = a_url_match.group(1)
                a_words = a_url.split('.')
                if a_words[-1].lower() in self.img_format:
                    urls.append(a_url)
        return urls

    def search_img_tag(self, html):
        if not html: return []
        # search tags
        img_tag_list = self.img_tag_pattern.findall(html)
         
        urls = []
        # search urls
        for img_tag in img_tag_list:
            img_url_match = self.img_link_pattern.search(img_tag)
            if img_url_match:
                img_url = img_url_match.group(1)
                img_words = img_url.split('.')
                if img_words[-1].lower() in self.img_format:
                    urls.append(img_url)
        return urls
