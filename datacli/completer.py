# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from prompt_toolkit.contrib.completers import WordCompleter

# TODO remove \c ?
keywords = [
    # sql
    'create', 'select', 'insert', 'drop', 'delete', 'from', 'where', 'table',
    # custom
    '\c help', '\c set'
]

MGOCompleter = WordCompleter(keywords, ignore_case=True)
