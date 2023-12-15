import nltk

from urllib.parse import urlparse

# Ignoring english stop words 
def filtered_sentence(sentence):
    english_stopwords = nltk.corpus.stopwords.words('english')
    return ' '.join(word for word in sentence.split() if word.lower() not in english_stopwords)

# Get domain name (example.com)
def get_domain_name(url):
    try:
        return urlparse(url).hostname
    except:
        return ''

