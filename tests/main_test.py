import subprocess
import os
import shutil
import requests

from common.constants import WORDS_BASE_PATH
from tests.expected_results import QUERY_RESULTS

def check_request():
    for query in QUERY_RESULTS:
        res = requests.get('http://localhost:5000/search?{}'.format(query))
        if res.content != QUERY_RESULTS[query]:
            return False


def main():
    childprocs = []
    try:
        articles_dir = './articles'
        print(os.path.abspath(articles_dir))
        raise Exception()
        articles_dir = '/Users/adif/development/amenity/tests/articles'

        childprocs.append(subprocess.Popen(['python3', 'server.py'], cwd='../src'))

        my_env = os.environ.copy()
        my_env["ARTICLES_DIR"] = articles_dir

        # subprocess.Popen(['docker', 'start'])  # TODO: docker too

        childprocs.append(subprocess.run(['redis-cli', 'FLUSHALL']))

        words_folder = WORDS_BASE_PATH
        for filename in os.listdir(words_folder):
            file_path = os.path.join(words_folder, filename)

            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        # subprocess.Popen(['docker', 'build', '-t', 'test_image', '.'], cwd='./images')
        childprocs.append(subprocess.run(['docker-compose', 'up', '--scale', 'worker=4', '--scale', 'writer=4'], cwd='../', env=my_env))

    finally:
        for p in childprocs:
            p.kill()

if __name__ == '__main__':
    # main()
    check_request()
    print('finish')
