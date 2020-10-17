import subprocess
import os
from common.constants import WORDS_BASE_PATH, SRC_BASE_PATH, PROJECT_BASE_PATH, WORKERS_COUNT


# TODO:
"""
+ check url pattern
+ print only on change
+ finish setup + test
+ check that it works from other directories
+ make services num dynamic
- add more input checks + robust
- add working print
- change prints and document
- put articles dir in main_test
- PEP8
- README

"""

def main():
    articles_dir = input('Please enter your articles directory: ')
    setup(articles_dir)


def setup(articles_dir):
    words_folder = './words'
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', './requirements'])

    for filename in os.listdir(words_folder):
        file_path = os.path.join(words_folder, filename)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    subprocess.run(['redis-cli', 'FLUSHALL'])

    childprocs = []
    try:
        workers_count = 4
        childprocs.append(subprocess.Popen(['python3', 'server.py'], cwd=SRC_BASE_PATH))

        my_env = os.environ.copy()
        my_env["ARTICLES_DIR"] = articles_dir
        my_env["FLASK_ENV"] = 'development'

        childprocs.append(subprocess.run(['docker', 'build', '-t', 'test_image', '.'],
                                         cwd=PROJECT_BASE_PATH))

        subprocess.run(['docker-compose', 'up', '--scale', 'worker={}'.format(WORKERS_COUNT), '--scale', 'writer={}'.format(WORKERS_COUNT)],
                       cwd=PROJECT_BASE_PATH, env=my_env)

    finally:
        for p in childprocs:
            if isinstance(p, subprocess.Popen):
                p.terminate()

if __name__ == '__main__':
    main()
