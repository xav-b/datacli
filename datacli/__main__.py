#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from __future__ import unicode_literals
from __future__ import print_function
import sys
import logging

import click
from traitlets.config.loader import Config
from IPython.terminal.embed import InteractiveShellEmbed
import pandas as pd
from pydrill.client import PyDrill
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.lexers.sql import MySqlLexer
from pygments.styles import get_style_by_name

from datacli.__init__ import __version__
from datacli.completer import MGOCompleter

EXIT_QUERIES = ['quit', 'exit']
BLACKLIST_QUERIES = ['']

log = logging.getLogger('datacli')
# documentation : https://ipython.org/ipython-doc/2/interactive/reference.html#embedding
# https://ipython.org/ipython-doc/1/config/ipython.html
ipcfg = Config()
ipshell = InteractiveShellEmbed(
    config=Config(),
    banner1='--> Dropping into IPython for interactive analysis',
    exit_msg='--> leaving interactive mode')

# default to docker style dns
DRILL_DEFAULT_HOST = 'drill'
DRILL_DEFAULT_PORT = 8047


def datacli_prompt(database, host, history, style='colorful'):
    prompt_style = '[ datacli::{uri}::{database} ] >>> '.format(uri=host, database=database)
    prompt_opts = {
        'completer': MGOCompleter,
        'history': history,
        'lexer': MySqlLexer,
        'auto_suggest': AutoSuggestFromHistory(),
        'style': get_style_by_name(style)
    }

    return prompt(prompt_style, **prompt_opts)


def configure_logger():
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)-6s :: %(levelname)-6s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)


def process_input(conn, db, query_tpl, is_interactive):
    opts = {
        'db': db
    }
    query = query_tpl.format(**opts)
    log.info('sending query to drill [{}]'.format(query))
    df = pd.DataFrame([row for row in conn.query(query)])
    print(df.head())
    print()
    if is_interactive:
        # drop an interpreter for analyzing results
        # IPython.embed(header='interactive query result analysis')
        ipshell('--> Hit Ctrl-D to exit interpreter and continue program.\n')


# TODO default sort order ?
@click.command()
@click.option('-H', '--host', default=DRILL_DEFAULT_HOST, envvar='DRILL_HOST',
              help='Host address of the drillbit server.')
@click.option('-p', '--port', default=DRILL_DEFAULT_PORT, envvar='DRILL_PORT',
              help='Port number of the drillbit server.')
@click.option('-v', '--version', is_flag=True, help='Version of datacli.')
@click.option('-i', '--interactive', is_flag=True,
              help='Drop into an ipython shell with query result.')
@click.argument('database', envvar='MGO_DB', nargs=1)
def cli(database, host, port, interactive, version):
    """Cli entry point."""
    if version:
        print('datacli version: {}'.format(__version__))
        sys.exit(0)

    configure_logger()

    conn = PyDrill(host=host, port=port)
    if not conn.is_active():
        log.error('unable to reach Drill server')
        return 1

    history = InMemoryHistory()
    log.info('connected to Drillbit')
    while True:
        try:
            query = datacli_prompt(database, host, history)
            query = query.lower()
            # TODO help
            if query in EXIT_QUERIES:
                log.warning('hit exit command')
                break
            elif query in BLACKLIST_QUERIES:
                log.warning('blacklisted query, skipping processing')
                continue

            process_input(conn, database, query, interactive)
        except KeyboardInterrupt:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed

    log.info('shutting down...')
    return 0

if __name__ == '__main__':
    sys.exit(cli())
