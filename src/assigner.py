import os

from ..api.queue_helper_redis_api import QueueHelperRedisAPI
from ..common.constants import ARTICLES_FOLDER


def assign(files_path):
    for filename in os.listdir(files_path):
        if filename.endswith('.json'):
            QueueHelperRedisAPI.add_file_name(filename)


def main():
    assign(ARTICLES_FOLDER)


if __name__ == '__main__':
    main()
