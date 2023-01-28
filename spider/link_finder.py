from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):
    def __init__(self, base_scrape_url, page_url, website_url):
        super().__init__()
        self.base_url = base_scrape_url
        self.website_url = website_url
        self.links = set()
        self.page_url = page_url
        self.meta_data = []
        self.header_titles = set()
        self.current_tag_is_header = False

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag in ("b", "h3"):
            for _ in attrs:
                content = attrs[0][1]
                if content == "whb":
                    self.current_tag_is_header = True
        else:
            self.current_tag_is_header = False

        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
        if tag == "meta":
            for (attribute, value) in attrs:
                if attribute == "name":
                    self.get_meta_info(value, list(attrs))

    def handle_data(self, data: str):
        if self.current_tag_is_header == True:
            self.header_titles.add(data)
            self.current_tag_is_header = False

    def parse_text_from_url(self):
        fallback_splitted = self.page_url.replace(
            self.website_url+'/', "").split('-')
        fallback = str.join(' ', fallback_splitted).split(':')
        if len(fallback) > 1:
            return fallback[1]
        return fallback[0]

    def set_not_null(self, a, b):
        if a == "":
            return b
        else:
            return a

    def get_meta_info(self, value, attrs):
        title = ""
        description = ""

        content = attrs[1][1]
        if ("title" in value) or ("description" in value):
            if "title" in value:
                title = content
            else:
                fallback_title = self.parse_text_from_url()
                title = fallback_title

            #  is current tag
            if "description" in value:
                description = content
            else:
                fallback_description = self.parse_text_from_url()
                description = fallback_description

            meta = {
                "title": title,
                "description": description,
                "url": self.page_url
            }
            self.meta_data.append(meta)

    def page_links(self):
        return self.links

    def page_meta_data(self):
        return self.meta_data

    def page_titles(self):
        return self.header_titles

    def error(self, message):
        pass
