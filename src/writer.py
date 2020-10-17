import time
import os

from ..api.queue_helper_redis_api import QueueHelperRedisAPI
from ..api.keyword_funnel_redis_api import KeywordFunnelRedisAPI
from ..common.constants import SLEEP_INTERVAL, WORDS_FOLDER


def main_loop():
    """
    wait for words with new articles to update their appropriate file
    """
    lastly_seen_word = True

    while True:
        word = QueueHelperRedisAPI.get_word_to_flush()

        if not word:
            if lastly_seen_word:
                lastly_seen_word = False
                print('wait for word')

            time.sleep(SLEEP_INTERVAL)
            continue

        lastly_seen_word = True

        articles = KeywordFunnelRedisAPI.get_all_articles_by_word(word)
        if not articles:
            continue

        # print('in writer:', word, articles)

        lock = QueueHelperRedisAPI.get_lock(word)
        with lock:
            write_articles_to_word(word, articles)


def write_articles_to_word(word, articles):
    word_file_path = os.path.join(WORDS_FOLDER, word.decode('ascii'))
    if os.path.exists(WORDS_FOLDER):
        try:
            with open(word_file_path, 'a+b') as f:
                f.writelines(article + b'\n' for article in articles)
        except FileNotFoundError as e:
            return


def main():
    main_loop()


if __name__ == '__main__':
    main_loop()
