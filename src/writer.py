import time
import os
import json

from ..api.queue_helper_redis_api import QueueHelperRedisAPI
from ..api.keyword_funnel_redis_api import KeywordFunnelRedisAPI
from ..common.constants import SLEEP_INTERVAL, WORDS_FOLDER

# SLEEP_INTERVAL = 1
# ARTICLES_FOLDER = '/articles'
# WORDS_FOLDER = '/tmp'

def main_loop():
    while True:
        word = QueueHelperRedisAPI.get_word_to_flush()

        if not word:
            print('wait for word')
            time.sleep(SLEEP_INTERVAL)
            continue

        articles = KeywordFunnelRedisAPI.get_all_articles_by_word(word)

        # print('in writer:', word, articles)

        lock = QueueHelperRedisAPI.get_lock(word)
        with lock:
            write_articles_to_word(word, articles)


def write_articles_to_word(word, articles):
    word_file_path = os.path.join(WORDS_FOLDER, word.decode('ascii'))

    with open(word_file_path, 'ab') as f:
        # print('writing:', word, [article + b'\n' for article in articles])
        f.writelines(article + b'\n' for article in articles)


def main():
    main_loop()


if __name__ == '__main__':
    print('start')
    main_loop()