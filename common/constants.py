import os

# TODO: get curr path and add

CONSTANTS_FILE_PATH = os.path.realpath(os.path.dirname(__file__))

SLEEP_INTERVAL = 0.01
MAX_ARTICLES_COUNT_IN_MEM = 200

OPERATORS = {'OR': set.update, 'AND': set.intersection_update}

WORDS_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../words')
REQUIREMENTS_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../requirements')
SRC_BASE_PATH = os.path.join(CONSTANTS_FILE_PATH, '../src')

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