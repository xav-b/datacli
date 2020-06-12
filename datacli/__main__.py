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
import mycli.main

from datacli.__init__ import __version__
from datacli.completer import MGOCompleter

BLACKLIST_QUERIES = ['']
# note : usuable with all requests
DEFAULT_TIMEOUT = 10
DEFAULT_PROMPT_TPL = '[{counter}][ datacli::{host}::{db} ] >>> '
SPECIAL_CMD_PREFIX = '\c'
# default to docker style dns
DRILL_DEFAULT_HOST = 'drill'
DRILL_DEFAULT_PORT = 8047
# syntax sugar for readibility
REPL_DONE = True

log = logging.getLogger('datacli')
# documentation :
#   https://ipython.org/ipython-doc/2/interactive/reference.html#embedding
#   https://ipython.org/ipython-doc/1/config/ipython.html
ipcfg = Config()
ipshell = InteractiveShellEmbed(
    config=Config(),
    banner1='--> Dropping into IPython for interactive analysis',
    exit_msg='--> leaving interactive mode')


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


def is_special_command(query):
    """Try to detect non-sql, custom commands supported."""
    return query.split()[0] == SPECIAL_CMD_PREFIX


class DataPrompt(object):

    def __init__(self):
        self._history = InMemoryHistory()
        self._suggest = AutoSuggestFromHistory()

    def refresh(self, **ctx):
        # TODO use a configuration file
        style = 'colorful'
        prompt_tpl = DEFAULT_PROMPT_TPL
        prompt_opts = {
            'completer': MGOCompleter,
            'history': self._history,
            'lexer': MySqlLexer,
            'auto_suggest': self._suggest,
            'style': get_style_by_name(style)
        }

        return prompt(prompt_tpl.format(**ctx), **prompt_opts)


class DataCli(object):

    def __init__(self, conn, db, prompt=None, timeout=DEFAULT_TIMEOUT):
        self._ctx = {
            'host': conn.transport.connection.base_url,
            'db': db,
            'counter': 0
        }
        self.conn = conn
        self.timeout = timeout
        self.prompt = prompt

    def sql_exec(self, query, is_interactive):
        log.debug('sending query to drill: "{}"'.format(query))
        # TODO pass a parameter from cli ?
        df = pd.DataFrame([
            row for row in self.conn.query(query, timeout=self.timeout)
        ])
        print(df.head())
        print()

        if is_interactive:
            # drop an interpreter for analyzing results
            # IPython.embed(header='interactive query result analysis')
            ipshell('--> Hit Ctrl-D to exit interpreter and continue program.\n')

    def repl(self, is_interactive=False):
        query = (self.prompt.refresh(**self._ctx)
                            .lower()
                            .replace(';', '')
                            .format(**self._ctx))
        # TODO help (special command ?)
        if mycli.main.quit_command(query):
            log.warning('hit exit command')
            return REPL_DONE
        elif query in BLACKLIST_QUERIES:
            log.warning('blacklisted query, skipping processing')
            return
        elif is_special_command(query):
            log.warning('special commands not yet implemented')
            return REPL_DONE

        self.sql_exec(query, is_interactive)
        self._ctx['counter'] += 1


# TODO custom prompt using global parameters
# TODO default sort order ?
@click.command()
@click.option('-H', '--host', default=DRILL_DEFAULT_HOST, envvar='DRILL_HOST',
              help='Host address of the drillbit server.')
@click.option('-p', '--port', default=DRILL_DEFAULT_PORT, envvar='DRILL_PORT',
              help='Port number of the drillbit server.')
@click.option('-t', '--timeout', default=DEFAULT_TIMEOUT, envvar='DRILL_TIMEOUT',
              help='HTTP requests timeout.')
@click.option('-v', '--version', is_flag=True, help='Version of datacli.')
@click.option('-i', '--interactive', is_flag=True,
              help='Drop into an ipython shell with query result.')
@click.argument('dbname', envvar='DATA_DB', nargs=1)
def cli(dbname, host, port, timeout, interactive, version):
    """Cli entry point."""
    if version or dbname == 'version':
        print('datacli version: {}'.format(__version__))
        sys.exit(0)

    configure_logger()

    conn = PyDrill(host=host, port=port)
    if not conn.is_active():
        log.error('unable to reach Drill server')
        return 1

    cli = DataCli(conn, dbname, DataPrompt(), timeout=timeout)

    log.info('connected to Drillbit')
    while True:
        try:
            should_exit = cli.repl(interactive)
            if should_exit:
                break
        except KeyboardInterrupt:
            break  # Control-C pressed
        except EOFError:
            break  # Control-D pressed

    log.info('shutting down...')
    return 0

if __name__ == '__main__':
    sys.exit(cli())
