import time
import os
import json
import string

from ..api.queue_helper_redis_api import QueueHelperRedisAPI
from ..api.keyword_funnel_redis_api import KeywordFunnelRedisAPI
from ..common.constants import ARTICLES_FOLDER, SLEEP_INTERVAL, MAX_ARTICLES_COUNT_IN_MEM

# SLEEP_INTERVAL = 1
# ARTICLES_FOLDER = '/articles'
# MAX_ARTICLES_COUNT_IN_MEM = 50

def main_loop():
    while True:
        file_name = QueueHelperRedisAPI.get_file_name()
        if not file_name:
            print('Reader waiting for new file')
            time.sleep(SLEEP_INTERVAL)
            continue

        article_title, words = seperate_article_words(file_name)

        for word in words:

            while KeywordFunnelRedisAPI.get_articles_count(word) > MAX_ARTICLES_COUNT_IN_MEM:
                time.sleep(SLEEP_INTERVAL)

            # print('adding:', word, article_title)
            KeywordFunnelRedisAPI.add_article_by_word(word, article_title)
            QueueHelperRedisAPI.add_word_to_flush(word)


def clean_word(word):
    printable = string.printable[:36]
    word = ''.join(filter(lambda c: c in printable, word))
    word = word.lower()
    return word


def seperate_article_words(file_name):
    file_path = os.path.join(ARTICLES_FOLDER, file_name.decode('ascii'))
    if not os.path.exists(file_path):
        return None, []

    with open(file_path, 'r') as f:
        data = json.load(f)
        if not 'title' in data or not 'text' in data:
            print('Bad json file: ', file_name)
            return None, []

        article_title = data['title']
        text = data['text']
        words = set(filter(lambda word: word != '', map(clean_word, text.split())))
        return article_title, words


def main():
    main_loop()


if __name__ == '__main__':
    print('start')
    main_loop()
