# TODO: get curr path and add

OPERATORS = {'OR': set.update, 'AND': set.intersection_update}
WORDS_BASE_PATH = '../words'
SLEEP_INTERVAL = 0.01
ARTICLES_FOLDER = '/articles'
MAX_ARTICLES_COUNT_IN_MEM = 50
WORDS_FOLDER = '/tmp'

BASIC_PAGE = """<!DOCTYPE html>
<html>
<body>
<pre>
{}
</pre>
</body>
</html>"""