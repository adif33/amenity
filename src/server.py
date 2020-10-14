from flask import Flask
from flask import request
from common.constants import OPERATORS, WORDS_BASE_PATH, BASIC_PAGE
import os


# OPERATORS = {'OR': set.update, 'AND': set.intersection_update}

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def get_handler():
    keywords = request.args.get('keywords')
    operator = request.args.get('operator')
    if not keywords or not operator:
        return 'bad request'

    # TODO: check keywords format (',' will break it)

    if operator not in OPERATORS:
        return 'bad operator'

    articles = get_articles(keywords, operator)
    print(keywords, operator)
    return BASIC_PAGE.format(articles)


def get_articles(keywords, operator):
    output = None  # TODO: what if no keywords?
    operator_func = OPERATORS[operator]

    for keyword in keywords.split(','):
        curr_word_path = os.path.join(WORDS_BASE_PATH, keyword)

        if not os.path.exists(curr_word_path):
            # TODO: handle
            continue

        with open(curr_word_path, 'r') as f:
            new_set = {article.rstrip('\n') for article in f.readlines()}

        if output == None:
            # TODO: find a better way
            output = new_set

        operator_func(output, new_set)

    return '\n'.join(output)


if __name__ == '__main__':
    app.run()
    # app.run(host= '0.0.0.0')
    # get_articles('', 'AND')