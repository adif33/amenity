import subprocess
import os
import time
import requests
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from common.constants import WORDS_BASE_PATH, REQUIREMENTS_BASE_PATH, SRC_BASE_PATH, PROJECT_BASE_PATH, \
    TEST_ARTICLES_BASE_PATH, WORKERS_COUNT

from tests.expected_results import QUERY_RESULTS

SLEEP_BEFORE_REQUESTS = 25


def main():
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', REQUIREMENTS_BASE_PATH])
    for filename in os.listdir(WORDS_BASE_PATH):
        file_path = os.path.join(WORDS_BASE_PATH, filename)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    subprocess.run(['redis-cli', 'FLUSHALL'])

    childprocs = []

    try:
        my_env = os.environ.copy()
        my_env["ARTICLES_DIR"] = TEST_ARTICLES_BASE_PATH
        my_env["WORDS_DIR"] = WORDS_BASE_PATH
        my_env["FLASK_ENV"] = 'development'
        childprocs.append(subprocess.Popen(['python3', 'server.py'], cwd=SRC_BASE_PATH, env=my_env))

        childprocs.append(subprocess.run(['docker', 'build', '-t', 'test_image', '.'], cwd=PROJECT_BASE_PATH))
        subprocess.Popen(['docker-compose', 'up', '--scale', 'worker={}'.format(WORKERS_COUNT), '--scale',
                          'writer={}'.format(WORKERS_COUNT)], cwd='./', env=my_env)

        time.sleep(SLEEP_BEFORE_REQUESTS)

        if check_request():
            print('Success!!\nAll tests passed.')
        else:
            print('Failed')

    finally:
        for p in childprocs:
            if isinstance(p, subprocess.Popen):
                p.terminate()


def check_request():
    for query in QUERY_RESULTS:
        res = requests.get('http://localhost:5000/search?{}'.format(query))

        if res.status_code != 200:
            print('Bad status code: ', res.status_code)
            return False

        result_articles = res.content[36:-23].split(b'\n')

        if len(result_articles) != len(QUERY_RESULTS[query]):
            return False

        for result_article in result_articles:
            if result_article not in QUERY_RESULTS[query]:
                return False

    return True


if __name__ == '__main__':
    main()
