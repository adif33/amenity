import subprocess
from src.add_articles import add_articles_from_path


# TODO:
"""
- mount articles for reader and assigner on the fly

"""

def main():
    articles_dir = '/Users/adif/development/adi_project/tests/articles'
    # subprocess.Popen(['docker', 'start'])
    # subprocess.Popen(['redis-server'])
    # clean server
    # subprocess.Popen(['docker', 'build', '-t', 'test_image', '.'], cwd='./images')
    subprocess.run(['docker-compose', 'up', '--scale', 'worker=4', '--scale', 'writer=4'], cwd='./images')
    # add_articles_from_path(articles_dir)

if __name__ == '__main__':
    main()
