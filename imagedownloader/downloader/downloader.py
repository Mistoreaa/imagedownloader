

import os
import platform
import time
from urllib import request, parse, error
from http import cookiejar

from config.config import Config


class Downloader():

    home_dir = os.path.expanduser('~')
    export_dir_name = 'DL_images'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) ' \
                 'AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25'

    def __init__(self, progress=None):
        self.progress = progress
        self.opener = self.__build_opener()
        self.post_param = None

    def set_post_param(self, post=None):
        if post:
            self.post_param = parse.urlencode(post).encode('utf-8')
        else:
            self.post_param = post

    def set_headers(self, headers):
        # headers: [(header-name, value), (...)]
        self.opener.addheaders = headers

    def download(self, url):
        req = request.Request(url)
        try:
            conn = self.opener.open(req, self.post_param)
        except error.URLError as e:
            raise
        return conn

    def download_html(self, url):
        req = request.Request(url)
        html = None
        try:
            conn = self.opener.open(req, self.post_param)
        except error.URLError as e:
            raise
        else:
            html = self.__convert_tounicode(conn.read())
        return html if html else ''

    def export(self, filepath, conn):
        if not conn:
            return
        with open(filepath, "wb") as img_file:
            img_file.write(conn.read())


    def export_images(self, urls):
        if not urls : return
        export_dirpath = self.__get_export_dirpath()
        try:
            os.mkdir(export_dirpath)
        except OSError as e:
            raise
        if self.progress:
            self.progress.set_max(len(urls))
        count = 0
        for url in urls:
            self.export(self.__make_export_filepath(export_dirpath, url),
                                                     self.download(url))
            count += 1
            if self.progress:
                self.progress.show(count)

    def login(self, url):
        self.download(url)

    def __convert_tounicode(self, string):
        charset = ('utf-8', 'euc_jp', 'shift_jis', 'iso2022jp', 'latin_1', 'ascii')
        decoded = ''
        for encoding in charset:
            try:
                decoded = string.decode(encoding)
                break
            except:
                pass
        return decoded

    def __build_opener(self):
        cj = cookiejar.CookieJar()
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', self.user_agent)]
        return opener

    def __get_path_delimiter(self):
        if platform.system() == 'Windows':
            return '\\'
        else:
            return '/'

    def __get_filename(self, url):
        if not url:
            return ''
        names = url.split('/')
        return names[-1]

    def __get_export_dirpath(self):
        if Config.EXPORT_DIR_PATH:
            return Config.EXPORT_DIR_PATH
        times = str(time.time()).split('.')
        delimiter = self.__get_path_delimiter()
        export_dir_path = []
        export_dir_path.append(self.home_dir)
        export_dir_path.append(delimiter)
        export_dir_path.append(self.export_dir_name)
        export_dir_path.append('_')
        export_dir_path.append(times[0])
        export_dir_path.append(delimiter)
        return ''.join(export_dir_path)

    def __make_export_filepath(self, dirpath, url):
        if not dirpath or not url:
            return ''
        path = []
        path.append(dirpath)
        path.append(self.__get_filename(url))
        return ''.join(path)
