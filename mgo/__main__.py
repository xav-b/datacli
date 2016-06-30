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
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.lexers.sql import MySqlLexer
from pygments.styles import get_style_by_name

from mgo.__init__ import __version__
from mgo.completer import MGOCompleter

log = logging.getLogger('mgocli')

# default to docker style dns
MONGO_DEFAULT_ADDR = 'mongo'


def connection(addr, database, user=None, never_prompt=False):
    db_uri = 'mongodb://{}/{}'.format(addr, database)
    conn = pymongo.MongoClient(db_uri)

    if user and not never_prompt:
        passwd_prompt = ' --> MongoDB password for user {}'.format(user)
        passwd = click.prompt(passwd_prompt, hide_input=True, show_default=False, type=str)
        conn[database].authenticate(user, password=passwd)

    return conn


def mgo_prompt(database, conn, style='colorful'):
    history = InMemoryHistory()
    prompt_style = '[ mgo::{uri}::{database} ] >>> '.format(uri=conn.address[0], database=database)
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


def process_input(db, query, row_limit):
    log.info('You said: %s' % query)
    cursor = db.appturbo_open.find().sort('_id', -1).limit(row_limit)
    for item in cursor:
        log.info(item)


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

    configure_logger()

    conn = connection(address, database, user, never_prompt)


    while True:
        try:
            query = mgo_prompt(database, conn)
            query = query.lower()
            if query == 'exit':
                break
            process_input(conn[database], query, row_limit)
        except KeyboardInterrupt:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed

    conn.close()
    log.info('Bye!')

if __name__ == '__main__':
    cli()
