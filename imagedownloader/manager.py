

import sys
import argparse

from downloader import downloader
from util import progress
from website import website
from website import general
from website import pixiv
from config.config import Config


class Manager():

    def __init__(self, downloader=None, site=None, has_progress=False):
        self.__sites = self.__build_sites()
        if downloader:
            self.downloader = downloader
        else:
            self.downloader = self.__build_downloader(has_progress)
        self.site = site

    def set_downloader(self, downloader):
        self.downloader = downloader

    def set_site(self, site):
        self.site = site

    def run_download(self):
        if not self.site:
            return
        if not self.site.is_logged:
            self.login()
        self.download()

    def run_download_order(self):
        pass

    def download(self):
        urls = self.site.parse_html(self.downloader.download_html(self.site.required_url))
        self.downloader.export_images(urls)

    def login(self):
        account = Config.ACCOUNT.get(self.site.__class__.__name__, None)
        if not account:
            return
        self.downloader.set_post_param(self.site.make_login_param(account))
        self.downloader.login(self.site.loginpage_url)
        self.downloader.set_headers([('Referer', self.site.domain)])
        self.site.is_logged = True
        self.downloader.set_post_param()

    def convert_param_to_site(self, param):
        site = self.build_specified_site(param)
        if site:
            return site
        else:
            return self.build_site(param.url)

    def build_site(self, url):
        for site in self.__sites:
            if site.host is None:
                continue
            else:
                if site.host in url:
                    site.set_required_url(url)
                    return site
        if self.site is None:
            return general.General(url)
        
    def build_specified_site(self, param):
        if not param:
            return None 
        if not isinstance(param, Param):
            return None

        if param.specify.lower() == 'pixiv':
            return site.Pixiv(param.url)
        else:
            return None

    def __build_downloader(self, has_progress=False):
        if has_progress:
            prg = progress.Progress()
        else:
            prg = None
        return downloader.Downloader(progress=prg)

    def __build_sites(self):
        sites = []
        sites.append(general.General())
        sites.append(pixiv.Pixiv())
        return sites


class Param():

    def __init__(self, url=None, req_id=None, req_pass=None, specify=None, order=None):
        self.url = url
        self.req_id = req_id
        self.req_pass = req_pass
        self.specify = specify
        if self.__check_order(order):
            self.order = order
        else:
            self.order = None

    def convert_todict(self, param):
        if not isinstance(param, dict):
            raise TypeError('not dict type')
        self.url = param.get('url', None)
        self.req_id = param.get('id', None)
        self.req_pass = param.get('pass', None)
        self.specify = param.get('specify', None)
        if self.__check_order(param.get('order', None)):
            self.order = param.get('order', None)
        else:
            self.order = None

    def __check_order(self, order):
        return False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, default='', help='web site url')
    parser.add_argument('-i', '--id', type=str, default='', help='login id')
    parser.add_argument('-p', '--pass', type=str, default='', help='login pass')
    parser.add_argument('-s', '--specify', type=str, default='', help='specified site')
    parser.add_argument('-o', '--order', type=str, default='', help='execution order')
    return parser.parse_args()


if __name__ == '__main__':
    param = parse_args()
    if not param.url:
        print('no url')
        sys.exit()
    print('download start')
    prm = Param()
    prm.convert_todict(vars(param))
    mng = Manager(has_progress=True)
    mng.set_site(mng.convert_param_to_site(prm))
    mng.run_download()
    print('\n')
    print('download finish')
