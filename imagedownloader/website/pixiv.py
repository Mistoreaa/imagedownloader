

import re
import time
import collections

from website import website

class Pixiv(website.WebSite):

    loginpage_url = 'https://www.secure.pixiv.net/login.php'

    # pattern
    manga_illust_id_pattern = re.compile('href[\s]*="/member_illust.php\?mode=manga&amp;illust_id=(.*?)"')
    mypage_illust_id_pattern = re.compile('href[\s]*="/member_illust.php\?mode=medium&amp;illust_id=(.*?)"')
    memberlist_illust_id_pattern = re.compile('href[\s]*="member_illust.php\?mode=big&amp;illust_id=(.*?)"')
    illust_storage_url_pattern = re.compile('http://i[0-9]+[.]pixiv[.]net/img[0-9]+/img/.*/(.*?)$')

    def __init__(self, url=None):
        super().__init__()
        self.domain = 'http://www.pixiv.net/'
        self.host = 'pixiv.net'
        self.required_url = url
        self.is_logged = False
        self.page_categories = self.__make_pagecategories()

    def set_required_url(self, url):
        if self.host in url: 
            self.required_url = url
        else:
            raise Exception('Required url do not match this class.')

    def parse_html(self, html):
        """return image urls"""
        action = self.__get_parse_action()
        if not action:
            return []
        return action(html)

    def discriminate_pagecategory(self):
        category = None
        for i, v in self.page_categories.items():
            if v in self.required_url:
                category = i
                break
        return category

    def make_login_param(self, account):
        param = {'pixiv_id' : account[0], 'pass' : account[1],
                 'mode' : 'login', 'skip' : 0,
                 'return_to' : self.domain}
        return param

    def __get_parse_action(self):
        category = self.discriminate_pagecategory()
        if category == 'mypage':
            return self.__action_mypage
        elif category == 'member_illust':
            return self.__action_member_illust
        elif category == 'member_top':
            return self.__action_member_top
        elif category == 'ranking':
            return self.__action_ranking
        else:
            return None

    def __action_mypage(self, html):
        """ not supported """
        return []

    def __action_member_illust(self, html):
        """ single illustration """
        """
        urls = []
        illust_url = self.domain + 'member_illust.php?mode=big&illust_id='
        illust_id = None
        a_tag_list = self.a_tag_pattern.findall(html)
        for a_tag in a_tag_list:
            illust_id_match = self.memberlist_illust_id_pattern.search(a_tag)
            if illust_id_match:
                illust_id = illust_id_match.group(1)
                if illust_id:
                    break
        if illust_id:
            urls.append(illust_url + illust_id)
        return urls
        """
        urls = []
        img_urls = self.search_img_tag(html)
        if not img_urls:
            return urls
        for img_url in img_urls:
            illust_url_match = self.illust_storage_url_pattern.search(img_url)
            if illust_url_match:
                # In order to obtain a large image of the original, processing the file name.
                img_file = illust_url_match.group(1)
                origin_file = img_file.replace('_m', '')
                temp_illust_url = illust_url_match.group(0)
                origin_illust_url = temp_illust_url.replace(img_file, origin_file)
                urls.append(origin_illust_url)
        return urls

    def __action_member_top(self, html):
        """ Structure of the page is the same as my page. """
        return self.__action_mypage(html)

    def __action_ranking(self, html):
        urls = []
        img_urls = self.search_img_tag(html)
        if not img_urls:
            return urls
        for img_url in img_urls:
            illust_url_match = self.illust_storage_url_pattern.search(img_url)
            if illust_url_match:
                # In order to obtain a large image of the original, processing the file name.
                img_file = illust_url_match.group(1)
                origin_file = img_file.replace('_240mw', '')
                temp_illust_url = illust_url_match.group(0)
                temp_illust_url2 = temp_illust_url.replace('mobile/', '')
                origin_illust_url = temp_illust_url2.replace(img_file, origin_file)
                urls.append(origin_illust_url)
        return urls

    def __make_pagecategories(self):
        page_categories = collections.OrderedDict()
        page_categories['mypage'] = 'mypage'
        page_categories['member_illust'] = 'member_illust'
        page_categories['member_top'] = 'member'
        page_categories['ranking'] = 'ranking'
        return page_categories
