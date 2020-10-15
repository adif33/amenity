import subprocess
import os
from src.server import start_server


# TODO:
"""
- mount articles for reader and assigner on the fly

"""

def main():
    # articles_dir = input('Please enter your articles directory:')
    # start_server()
    subprocess.Popen(['python3', 'server.py'], cwd='./src')
    articles_dir = '/Users/adif/development/amenity/tests/articles'
    my_env = os.environ.copy()
    my_env["ARTICLES_DIR"] = articles_dir
    # subprocess.Popen(['docker', 'start'])
    subprocess.run(['redis-cli', 'FLUSHALL'])
    # clean server
    # subprocess.Popen(['docker', 'build', '-t', 'test_image', '.'], cwd='./images')
    subprocess.run(['docker-compose', 'up', '--scale', 'worker=4', '--scale', 'writer=4'], cwd='./', env=my_env)

if __name__ == '__main__':
    main()
