import subprocess
import os
from common.constants import SRC_BASE_PATH, PROJECT_BASE_PATH, WORKERS_COUNT, WORDS_BASE_PATH


def main():
    articles_dir = input('Please enter your articles directory: ')
    if not os.path.isdir(articles_dir):
        print('Please insert a valid directory.')
        return
    setup(articles_dir)


def setup(articles_dir):
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', './requirements'])

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
        my_env["ARTICLES_DIR"] = articles_dir
        my_env["FLASK_ENV"] = 'development'

        childprocs.append(subprocess.Popen(['python3', 'server.py'], cwd=SRC_BASE_PATH, env=my_env))

        childprocs.append(subprocess.run(['docker', 'build', '-t', 'test_image', '.'],
                                         cwd=PROJECT_BASE_PATH))

        subprocess.run(['docker-compose', 'up', '--scale', 'worker={}'.format(WORKERS_COUNT), '--scale',
                        'writer={}'.format(WORKERS_COUNT)],
                       cwd=PROJECT_BASE_PATH, env=my_env)

    finally:
        for p in childprocs:
            if isinstance(p, subprocess.Popen):
                p.terminate()


if __name__ == '__main__':
    main()
