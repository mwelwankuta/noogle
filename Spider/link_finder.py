from html.parser import HTMLParser
from urllib import parse

def set_not_null(a, b) -> str:
    if a == "":
        return b
    else:
        return a


class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.meta_data =[] 

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
        if tag == "meta":
            for (attribute, value) in attrs:
                if attribute == "name":
                    self.get_meta_info(value, list(attrs))

    def get_meta_info(self, value, attrs):
        title = ""
        description = ""

        content = attrs[1][1]
        if ("title" in value) or ("description" in value):
            if ("title" in value) and ("description" not in value):
                title = content
            else:
                title_no_domain = self.page_url.replace(self.base_url+"/", "").split('-')
                fallback_title = str.join(' ', title_no_domain)
                title = fallback_title

            if (("twitter:description" in value) or ("description" in value)) and "title" not in value:
                description_no_domain = self.page_url.replace(self.base_url+"/","").split('-')
                fallback_description = str.join(' ', description_no_domain)
                description = set_not_null(content,fallback_description)
            meta = {"title": title, "description": description, "url": self.page_url}
            self.meta_data.append(meta)

    def page_links(self):
        return self.links

    def page_meta_data(self):
        return self.meta_data

    def error(self, message):
        pass
