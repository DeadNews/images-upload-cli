# py-image-uploader

> Upload images via APIs

[![PyPI version](https://img.shields.io/pypi/v/py-image-uploader)](https://pypi.org/project/py-image-uploader)
[![CI/CD](https://github.com/DeadNews/py-image-uploader/actions/workflows/python-app.yml/badge.svg)](https://github.com/DeadNews/py-image-uploader/actions/workflows/python-app.yml)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/DeadNews/py-image-uploader/main.svg)](https://results.pre-commit.ci/latest/github/DeadNews/py-image-uploader/main)
[![codecov](https://codecov.io/gh/DeadNews/py-image-uploader/branch/main/graph/badge.svg?token=OCZDZIYPMC)](https://codecov.io/gh/DeadNews/py-image-uploader)

## Hostings

| host                                  | key required | return example                                         |
| :------------------------------------ | :----------: | :----------------------------------------------------- |
| [catbox](https://catbox.moe/)         |      -       | https://files.catbox.moe/%7Bid%7D                      |
| [fastpic](https://fastpic.org/)       |      -       | https://i120.fastpic.org/big/2022/0730/d9/%7Bid%7D.png |
| [filecoffee](https://file.coffee/)    |      -       | https://file.coffee/u/%7Bid%7D.png                     |
| [freeimage](https://freeimage.host/)  |      -       | https://iili.io/%7Bid%7D.png                           |
| [geekpic](https://geekpic.net/)       |      -       | https://s01.geekpic.net/%7Bid%7D.png                   |
| [gyazo](https://gyazo.com/)           |      +       | tba                                                    |
| [imageban](https://imageban.ru/)      |      +       | https://i2.imageban.ru/out/2022/07/30/%7Bid%7D.png     |
| [imgbb](https://imgbb.com/)           |      +       | https://i.ibb.co/%7Bid%7D/image.png                    |
| [imgchest](https://imgchest.com/)     |      +       | https://cdn.imgchest.com/files/%7Bid%7D.png            |
| [imgur](https://imgur.com/)           |      +       | https://i.imgur.com/%7Bid%7D.png                       |
| [pictshare](https://pictshare.net/)   |      -       | https://pictshare.net/%7Bid%7D.png                     |
| [pixeldrain](https://pixeldrain.com/) |      -       | https://pixeldrain.com/api/file/%7Bid%7D               |
| [pixhost](https://pixhost.to/)        |      -       | https://img75.pixhost.to/images/69/%7Bid%7D_img.png    |
| [ptpimg](https://ptpimg.me/)          |      +       | https://ptpimg.me/%7Bid%7D.png                         |
| [up2sha](https://up2sha.re/)          |      +       | https://up2sha.re/media/raw/%7Bid%7D.png               |
| [uploadcare](https://uploadcare.com/) |      +       | https://ucarecdn.com/%7Bid%7D/img.png                  |

## Installation

```sh
pip install py-image-uploader
```

or

```sh
pipx install py-image-uploader
```

## Usage

```sh
Usage: py-image-uploader [OPTIONS] [IMAGES]...

  Upload images via APIs. The result will be copied to the clipboard.

Options:
  -h, --hosting [catbox|fastpic|filecoffee|freeimage|geekpic|gyazo|imageban|imgbb|imgchest|imgur|pictshare|pixeldrain|pixhost|ptpimg|up2sha|uploadcare]
                                  [default: geekpic]
  -b, --bbcode                    Add bbcode tags
  -t, --thumbnail                 Add thumbnails and bbcode tags
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

## Env variables

```ini
CAPTION_FONT= # default arial.ttf

BEEIMG_KEY=
FREEIMAGE_KEY=
GYAZO_TOKEN=
IMAGEBAN_TOKEN=
IMGBB_KEY=
IMGCHEST_KEY=
IMGUR_CLIENT_ID=
PTPIMG_KEY=
UP2SHA_KEY=
UPLOADCARE_KEY=
```

You can set these in environment variables, or in `.env` file:

- Unix: `~/.config/py-image-uploader/.env`
- MacOS: `~/Library/Application Support/py-image-uploader/.env`
- Windows: `C:\Users\<user>\AppData\Roaming\py-image-uploader\.env`
