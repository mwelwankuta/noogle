from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        return urlparse(url).hostname
    except:
        return ''
