from urllib.request import urlopen
from crawler.utilities import file_to_set, create_data_files, create_project_dir,use_path,set_to_file
from crawler.links import LinkFinder
from shared.utilities import get_domain_name
from database.connection import conn

class Bot:
    project_name = ""
    base_url = ""
    website_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name, website_url):
        Bot.project_name = project_name
        Bot.base_url = base_url
        Bot.domain_name = domain_name
        Bot.queue_file = Bot.project_name + "/queue.txt"
        Bot.crawled_file = Bot.project_name + "/crawled.txt"
        Bot.website_url = website_url
        self.boot()
        self.crawl_page("First spider", Bot.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(use_path(Bot.project_name))
        create_data_files(use_path(Bot.project_name), Bot.base_url)
        Bot.queue = file_to_set(Bot.queue_file)
        Bot.crawled = file_to_set(Bot.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Bot.crawled:
            print(thread_name + " now crawling " + page_url)
            print(
                "Queue "
                + str(len(Bot.queue))
                + " | Crawled  "
                + str(len(Bot.crawled))
            )
            Bot.add_links_to_queue(Bot.gather_links(page_url))
            Bot.queue.remove(page_url)
            Bot.crawled.add(page_url)
            Bot.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ""
        try:
            response = urlopen(page_url)
            if "text/html" in response.getheader("Content-Type"):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Bot.base_url, page_url, Bot.website_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()

        page_meta_data = finder.page_meta_data()
        page_header_titles = finder.page_titles()
        Bot.save_page_info(page_meta_data, page_header_titles)
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Bot.queue) or (url in Bot.crawled):
                continue
            if Bot.domain_name != get_domain_name(url):
                continue
            Bot.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Bot.queue, Bot.queue_file)
        set_to_file(Bot.crawled, Bot.crawled_file)

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
