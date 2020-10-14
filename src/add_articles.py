import subprocess

def add_articles_from_path(articles_dir):
    print('add_articles_from_path')
    # articles_dir = input('Article directory:')
    # articles_dir = '/Users/adif/development/adi_project/tests/articles'
    # docker
    # run - -rm - it - v / Users / adif / development / amenity / tests / articles: / articles
    # test_image
    # python / code / assigner.py
    subprocess.Popen(['docker', 'run', '--rm', '-it', '-v', '{}:/articles'.format(articles_dir), 'test_image', 'python', '-u', '/code/assigner.py'])