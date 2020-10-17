import os

CONSTANTS_FILE_PATH = os.path.realpath(os.path.dirname(__file__))

SLEEP_INTERVAL = 0.01
MAX_ARTICLES_COUNT_IN_MEM = 200
WORKERS_COUNT = '4'

OPERATORS = {'OR': set.update, 'AND': set.intersection_update}

WORDS_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../words')
REQUIREMENTS_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../requirements')
SRC_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../src')
PROJECT_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '..')
TEST_ARTICLES_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../tests/articles')

ARTICLES_FOLDER = '/articles'
WORDS_FOLDER = '/tmp'

BASIC_PAGE = """<!DOCTYPE html>
<html>
<body>
<pre>
{}
</pre>
</body>
</html>"""
