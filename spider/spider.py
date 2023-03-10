from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from database.database import conn
import os


class Spider:

    project_name = ""
    base_url = ""
    website_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name, website_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        Spider.website_url = website_url
        self.boot()
        self.crawl_page("First spider", Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(use_path(Spider.project_name))
        create_data_files(use_path(Spider.project_name), Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " now crawling " + page_url)
            print(
                "Queue "
                + str(len(Spider.queue))
                + " | Crawled  "
                + str(len(Spider.crawled))
            )
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ""
        try:
            response = urlopen(page_url)
            if "text/html" in response.getheader("Content-Type"):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url, Spider.website_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()

        page_meta_data = finder.page_meta_data()
        page_header_titles = finder.page_titles()
        Spider.save_page_info(page_meta_data, page_header_titles)
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def format_stored_meta_data(meta_info):
        meta_data = []
        for idx, meta_item in enumerate(meta_info):
            values = list(meta_item.values())
            if idx != len(meta_info) - 1:
                meta_data.append(
                    f"('{values[0]}','{values[1]}','{values[2]}'),")
            meta_data.append("(f'({values[0]}','{values[1]}','{values[2]})'")
        meta_as_str = ''.join(map(str, meta_data))
        return meta_as_str

    # Saves gather meta info to database
    @staticmethod
    def save_page_info(meta_info, header_titles):
        cursor = conn.cursor()
        for link in meta_info:
            title = link["title"]
            description = link["description"]
            url = link["url"]

            sql_meta = "insert into meta ('title', 'description', 'url') values (?, ?, ?);"
            cursor.execute(sql_meta, (title, description, url))

            meta_id = cursor.lastrowid

            for title in header_titles:
                more_than_one_word = len(title.split(' ')) > 1
                if more_than_one_word:
                    sql_header = "insert into titles ('meta_id', 'title') values (?, ?);"
                    cursor.execute(sql_header, (meta_id, title))
        conn.commit()
        cursor.close()
