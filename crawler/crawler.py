import threading
import multiprocessing

from queue import Queue
from crawler.utilities import *
from shared.utilities import get_domain_name
from shared.log import setup_custom_logger
from crawler.bot import Bot
logger = setup_custom_logger('root')

NUMBER_OF_THREADS = multiprocessing.cpu_count()
queue = Queue()

PROJECT_NAME = "wikihow"
HOMEPAGE = "https://www.wikihow.com/Main-Page"
WEBSITE_URL = "https://www.wikihow.com"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"

Bot(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, WEBSITE_URL)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Bot.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        msg = str(len(queued_links)) + " links in the queue"
        logger.debug(f"crawl(): {msg}")
        create_jobs()