#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from __future__ import unicode_literals
from __future__ import print_function
import sys

import click
from prompt_toolkit import prompt

from mgo.__init__ import __version__

# default to docker style dns
MONGO_DEFAULT_HOST = 'mongodb'
MONGO_DEFAULT_PORT = 27017


@click.command()
@click.option('-h', '--host', default='mongodb', envvar='MGO_HOST',
              help='Host address of the mongodb database.')
@click.option('-p', '--port', default=MONGO_DEFAULT_PORT, help='Port number at which the '
              'postgres instance is listening.', envvar='MGO_PORT')
@click.option('-u', '--user', envvar='MGO_USER',
              help='User name to connect to the postgres database.')
@click.option('-w', '--password', 'prompt_passwd', is_flag=True, default=False,
              help='Force password prompt.')
@click.option('-w', '--no-password', 'never_prompt', is_flag=True,
              default=False, help='Never prompt for password.')
@click.option('-v', '--version', is_flag=True, help='Version of pgcli.')
@click.argument('database', default=lambda: None, envvar='MGO_DB', nargs=1)
def cli(database, host, port, user, prompt_passwd, never_prompt, version):
    """Cli entry point."""
    if version:
        print('Version:', __version__)
        sys.exit(0)

    prompt_style = 'mongodb://{host}:{port}/{database} > '.format(
        host=host, port=port, database=database)
    answer = prompt(prompt_style)
    print('You said: %s' % answer)

if __name__ == '__main__':
    cli()
