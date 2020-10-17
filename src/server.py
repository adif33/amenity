from flask import Flask, request
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../'))
from common.constants import OPERATORS, WORDS_BASE_PATH, BASIC_PAGE

import string
import os


app = Flask(__name__)


@app.route('/search', methods=['GET'])
def get_handler():
    keywords = request.args.get('keywords')
    operator = request.args.get('operator')

    input_errors = check_search_args(keywords, operator)

    if input_errors:
        return BASIC_PAGE.format(input_errors)

    articles = get_articles(keywords, operator)
    return BASIC_PAGE.format(articles)


def check_search_args(keywords, operator):
    if not keywords or not operator:
        return 'Bad request format'

    if operator not in OPERATORS:
        return 'Please use valid operator: {}'.format([key for key in OPERATORS.keys()])

    allowed_chars = string.printable[:36]

    for word in keywords.split(','):
        if not word:
            return "Please don't use empty words"

        for c in word:
            if c not in allowed_chars:
                return 'Please use only English characters and numbers'

def get_articles_by_word(word):
    word_path = os.path.join(WORDS_BASE_PATH, word)

    if not os.path.exists(word_path):
        return set()

    with open(word_path, 'r') as f:
        return {article.rstrip('\n') for article in f.readlines()}

def get_articles(keywords, operator):
    operator_func = OPERATORS[operator]

    if not keywords:
        pass

    output = get_articles_by_word(keywords[0])

    for word in keywords.split(','):
        new_articles_set = get_articles_by_word(word)

        operator_func(output, new_articles_set)

    if not output:
        return 'No results found'

    return '--- ' + '\n--- '.join(output)


def start_server():
    app.run()


if __name__ == '__main__':
    app.run()
    # app.run(host= '0.0.0.0')
    # get_articles('', 'AND')