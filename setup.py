import subprocess
import os
from common.constants import WORDS_BASE_PATH



# TODO:
"""
+ check url pattern
- print only on change
- finish setup + test
- check that it works from other directories
- PEP8
- README

"""

def main():
    childprocs = []
    try:
        # articles_dir = input('Please enter your articles directory: ')
        articles_dir = '/private/tmp/out/'
        articles_dir = './tests/articles'

        words_folder = './words'

        subprocess.run(['python3', 'pip', 'install', '-r', './requierments'])

        for filename in os.listdir(words_folder):
            file_path = os.path.join(words_folder, filename)

            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        childprocs.append(subprocess.Popen(['python3', 'server.py'], cwd='./src'))



        # childprocs.append(subprocess.Popen(['docker', 'start']))
        subprocess.run(['redis-cli', 'FLUSHALL'])

        my_env = os.environ.copy()
        my_env["ARTICLES_DIR"] = articles_dir

        childprocs.append(subprocess.run(['docker', 'build', '-t', 'test_image', '.'], cwd='./'))
        subprocess.run(['docker-compose', 'up', '--scale', 'worker=4', '--scale', 'writer=4'], cwd='./', env=my_env)
    finally:
        for p in childprocs:
            p.kill()

if __name__ == '__main__':
    main()
