# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from prompt_toolkit.contrib.completers import WordCompleter

MGOCompleter = WordCompleter([
    'create', 'select', 'insert', 'drop',
    'delete', 'from', 'where', 'table'], ignore_case=True)
