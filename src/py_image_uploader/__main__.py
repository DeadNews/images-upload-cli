#!/usr/bin/env python
"""
Entry point for cli, enables execution with `python -m py_image_uploader`
"""
from os.path import dirname
from sys import argv

from .cli import main

if __name__ == "__main__":
    # Make sure the cli-parser does not print out __main__.py
    argv[0] = dirname(argv[0])

    main()
