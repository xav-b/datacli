# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sure

import datacli

META_INFO = ['__project__', '__author__', '__version__', '__licence__']

def test_package_metadatas():
    for info in META_INFO:
        hasattr(datacli, info).should.be.ok

def test_semantic_versioning():
    datacli.__version__.split('.').should.have.length_of(3)
