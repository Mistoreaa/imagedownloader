

from website import website

class General(website.WebSite):

    def __init__(self, url=None):
        super().__init__()
        self.required_url = url

    def parse_html(self, html):
        if not html:
            return []

        urls = self.search_a_tag(html)
        urls.extend(self.search_img_tag(html))
        return urls
