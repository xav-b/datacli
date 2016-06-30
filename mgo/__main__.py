#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from __future__ import unicode_literals
from __future__ import print_function
import sys
import logging

import click
import pymongo
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from pygments.lexers.sql import MySqlLexer

from mgo.__init__ import __version__
from mgo.completer import MGOCompleter

log = logging.getLogger('mgocli')

# default to docker style dns
MONGO_DEFAULT_ADDR = 'mongo'


def is_connected(conn, debug=False):
    try:
        info = conn.server_info()
        print('successfully connected')
        if debug:
            print(info)
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
        return false

    return True


def connection(addr, database, user=None, never_prompt=False):
    db_uri = 'mongodb://{}/{}'.format(addr, database)
    conn = pymongo.MongoClient(db_uri)

    if user and not never_prompt:
        passwd = click.prompt('Password', hide_input=True, show_default=False, type=str)
        conn[database].authenticate(user, password=passwd)

    if not is_connected(conn):
        sys.exit(1)

    return conn


def process_input(query):
    print('You said: %s' % query)


# TODO default docs limit ?
# TODO default sort order ?
@click.command()
@click.option('-a', '--address', default=MONGO_DEFAULT_ADDR, envvar='MGO_HOST',
              help='Host address of the mongodb database.')
@click.option('-u', '--user', envvar='MGO_USER',
              help='User name to connect to the postgres database.')
@click.option('-w', '--no-password', 'never_prompt', is_flag=True,
              default=False, help='Never prompt for password.')
@click.option('-v', '--version', is_flag=True, help='Version of pgcli.')
@click.option('-r', '--row-limit', default=10, envvar='MGO_ROW_LIMIT', type=click.INT,
              help='Set threshold for row limit prompt')
@click.argument('database', envvar='MGO_DB', nargs=1)
def cli(database, address, user, never_prompt, version, row_limit):
    """Cli entry point."""
    if version:
        print('mgocli version: {}'.format(__version__))
        sys.exit(0)

    conn = connection(address, database, user, never_prompt)

    prompt_style = '[ {uri}/{database} ] >>> '.format(uri=conn.address, database=database)
    history = InMemoryHistory()
    prompt_opts = {
        'completer': MGOCompleter,
        'history': history,
        'lexer': MySqlLexer
    }

    while True:
        try:
            query = prompt(prompt_style, **prompt_opts)
            query = query.lower()
            if query == 'exit':
                break
            process_input(query)
        except KeyboardInterrupt as err:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed
    print('Bye!')

if __name__ == '__main__':
    cli()
