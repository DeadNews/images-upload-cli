#!/usr/bin/env python
"""Entrypoint for cli, enables execution with `python -m images_upload_cli`."""
from images_upload_cli.cli import cli

if __name__ == "__main__":
    cli()
