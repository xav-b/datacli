#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from __future__ import unicode_literals
from __future__ import print_function
import sys
import logging

import click
from pydrill.client import PyDrill
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.lexers.sql import MySqlLexer
from pygments.styles import get_style_by_name

from mgo.__init__ import __version__
from mgo.completer import MGOCompleter

log = logging.getLogger('mgocli')

# default to docker style dns
DRILL_DEFAULT_HOST = 'drill'
DRILL_DEFAULT_PORT = 8047


def mgo_prompt(database, host, style='colorful'):
    history = InMemoryHistory()
    prompt_style = '[ mgo::{uri}::{database} ] >>> '.format(uri=host, database=database)
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


def process_input(conn, query):
    log.info('sending query to drill [{}]'.format(query))
    for res in conn.query(query):
        print(res)


# TODO default sort order ?
@click.command()
@click.option('-H', '--host', default=DRILL_DEFAULT_HOST, envvar='DRILL_HOST',
              help='Host address of the drillbit server.')
@click.option('-p', '--port', default=DRILL_DEFAULT_PORT, envvar='DRILL_PORT',
              help='Port number of the drillbit server.')
@click.option('-v', '--version', is_flag=True, help='Version of pgcli.')
@click.option('-r', '--row-limit', default=10, envvar='MGO_ROW_LIMIT', type=click.INT,
              help='Set threshold for row limit prompt')
@click.argument('database', envvar='MGO_DB', nargs=1)
def cli(database, host, port, row_limit, version):
    """Cli entry point."""
    if version:
        print('mgocli version: {}'.format(__version__))
        sys.exit(0)

    configure_logger()

    conn = PyDrill(host=host, port=port)
    if not conn.is_active():
        log.error('unable to reach Drill server')
        return 1

    log.info('connected to Drillbit')
    while True:
        try:
            query = mgo_prompt(database, conn)
            query = query.lower()
            if query == 'exit':
                break
            process_input(conn, query)
        except KeyboardInterrupt:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed

    conn.close()
    log.info('Bye!')
    return 0

if __name__ == '__main__':
    sys.exit(cli())
