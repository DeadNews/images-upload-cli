# py-image-uploader

> Upload images via APIs

[![PyPI version](https://img.shields.io/pypi/v/py-image-uploader)](https://pypi.org/project/py-image-uploader)
[![python-app](https://github.com/DeadNews/py-image-uploader/workflows/python-app/badge.svg)](https://github.com/DeadNews/py-image-uploader/actions)
[![python-codeql](https://github.com/DeadNews/py-image-uploader/workflows/python-codeql/badge.svg)](https://github.com/DeadNews/py-image-uploader/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeadNews/py-image-uploader/main.svg)](https://results.pre-commit.ci/latest/github/DeadNews/py-image-uploader/main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DeadNews_py-image-uploader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DeadNews_py-image-uploader)

## Hostings

- Works out of the box:

  - fastpic
  - geekpic
  - pixhost

- Key required:

  - freeimage
  - imageban
  - imageshack
  - imgbb
  - imgur
  - uploadcare

## Installation

```sh
pip install py-image-uploader
py-image-uploader --help
```

## Usage

```help
Usage: py-image-uploader [OPTIONS] [IMAGES]...

  Upload images via APIs

Options:
  -h, --hosting [fastpic|freeimage|geekpic|imageban|imageshack|imgbb|imgur|pixhost|uploadcare]
                                  [default: geekpic]
  -b, --bbcode                    Add bbcode tags
  -t, --thumbnail                 Add thumbnails and bbcode tags
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

## .env variables

You can set these in environment variables, or by creating `.env` in the app_dir.

```env
CAPTION_FONT=

FREEIMAGE_KEY=
IMAGEBAN_TOKEN=
IMAGESHACK_KEY=
IMGBB_KEY=
IMGUR_CLIENT_ID=
UPLOADCARE_KEY=
```

app_dir:

- Unix: `~/.config/py-image-uploader`
- MacOS: `~/Library/Application Support/py-image-uploader`
- Windows: `C:\Users\<user>\AppData\Roaming\py-image-uploader`
