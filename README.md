# images-upload-cli

> Upload images via APIs

[![PyPI version](https://img.shields.io/pypi/v/images-upload-cli)](https://pypi.org/project/images-upload-cli)
[![AUR version](https://img.shields.io/aur/version/python-images-upload-cli)](https://aur.archlinux.org/packages/python-images-upload-cli)
[![Main](https://github.com/DeadNews/images-upload-cli/actions/workflows/main.yml/badge.svg)](https://github.com/DeadNews/images-upload-cli/actions/workflows/main.yml)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/DeadNews/images-upload-cli/main.svg)](https://results.pre-commit.ci/latest/github/DeadNews/images-upload-cli/main)
[![codecov](https://codecov.io/gh/DeadNews/images-upload-cli/branch/main/graph/badge.svg?token=OCZDZIYPMC)](https://codecov.io/gh/DeadNews/images-upload-cli)

## Installation

PyPI

```sh
pip install images-upload-cli
# or
pipx install images-upload-cli
```

AUR

```sh
yay -S python-images-upload-cli
```

## Hostings

| host                                  | key required | return example                                       |
| :------------------------------------ | :----------: | :--------------------------------------------------- |
| [anhmoe](https://anh.moe/)            |      -       | `https://cdn.anh.moe/c/{id}.png`                     |
| [beeimg](https://beeimg.com/)         |      -       | `https://beeimg.com/images/{id}.png`                 |
| [catbox](https://catbox.moe/)         |      -       | `https://files.catbox.moe/{id}`                      |
| [fastpic](https://fastpic.org/)       |      -       | `https://i120.fastpic.org/big/2022/0730/d9/{id}.png` |
| [filecoffee](https://file.coffee/)    |      -       | `https://file.coffee/u/{id}.png`                     |
| [freeimage](https://freeimage.host/)  |      -       | `https://iili.io/{id}.png`                           |
| [gyazo](https://gyazo.com/)           |      +       | `https://i.gyazo.com/{id}.png`                       |
| [imageban](https://imageban.ru/)      |      +       | `https://i2.imageban.ru/out/2022/07/30/{id}.png`     |
| [imagebin](https://imagebin.ca/)      |      -       | `https://ibin.co/{id}.png`                           |
| [imgbb](https://imgbb.com/)           |      +       | `https://i.ibb.co/{id}/image.png`                    |
| [imgchest](https://imgchest.com/)     |      +       | `https://cdn.imgchest.com/files/{id}.png`            |
| [imgur](https://imgur.com/)           |      -       | `https://i.imgur.com/{id}.png`                       |
| [lensdump](https://lensdump.com/)     |      +       | `https://i.lensdump.com/i/{id}.png`                  |
| [pixeldrain](https://pixeldrain.com/) |      -       | `https://pixeldrain.com/api/file/{id}`               |
| [pixhost](https://pixhost.to/)        |      -       | `https://img75.pixhost.to/images/69/{id}_img.png`    |
| [ptpimg](https://ptpimg.me/)          |      +       | `https://ptpimg.me/{id}.png`                         |
| [smms](https://sm.ms/)                |      +       | `https://s2.loli.net/2022/07/30/{id}.png`            |
| [sxcu](https://sxcu.net/)             |      -       | `https://sxcu.net/{id}.png`                          |
| [telegraph](https://telegra.ph/)      |      -       | `https://telegra.ph/file/{id}.png`                   |
| [thumbsnap](https://thumbsnap.com/)   |      +       | `https://thumbsnap.com/i/{id}.png`                   |
| [tixte](https://tixte.com/)           |      +       | `https://{domain}.tixte.co/r/{id}.png`               |
| [up2sha](https://up2sha.re/)          |      +       | `https://up2sha.re/media/raw/{id}.png`               |
| [uplio](https://upl.io/)              |      +       | `https://upl.io/i/{id}.png`                          |
| [uploadcare](https://uploadcare.com/) |      +       | `https://ucarecdn.com/{id}/img.png`                  |
| [vgy](https://vgy.me/)                |      +       | `https://i.vgy.me/{id}.png`                          |

## Usage

```sh
Usage: images-upload-cli [OPTIONS] IMAGES...

  Upload images via APIs.

Options:
  -h, --hosting [anhmoe|beeimg|catbox|fastpic|filecoffee|freeimage|gyazo|imageban|imagebin|imgbb|imgchest|imgur|lensdump|pixeldrain|pixhost|ptpimg|smms|sxcu|telegraph|thumbsnap|tixte|up2sha|uplio|uploadcare|vgy]
                                  [default: imgur]
  -f, --format [plain|bbcode|html|markdown]
                                  The format of the links to be generated.  [default: plain]
  -t, --thumbnail                 Create captioned thumbnails. By default, in bbcode format.
  -n, --notify                    Send desktop notification on completion. Required libnotify.
  -c, --clipboard / -C, --no-clipboard
                                  Copy the result to the clipboard. Enabled by default.
  --env-file FILE                 The path to the environment file. Take precedence over the default config file.
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Use DEBUG to show debug logs. Use CRITICAL to suppress all logs.  [default: INFO]
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

## Env variables

```ini
CAPTION_FONT= # The default font is system dependent.

FREEIMAGE_KEY=
GYAZO_TOKEN=
IMAGEBAN_TOKEN=
IMGBB_KEY=
IMGCHEST_KEY=
IMGUR_CLIENT_ID=
LENSDUMP_KEY=
PTPIMG_KEY=
SMMS_KEY=
THUMBSNAP_KEY=
TIXTE_KEY=
UP2SHA_KEY=
UPLIO_KEY=
UPLOADCARE_KEY=
VGY_KEY=
```

You can set these in environment variables, or in `.env` file:

- Unix: `~/.config/images-upload-cli/.env`
- MacOS: `~/Library/Application Support/images-upload-cli/.env`
- Windows: `C:\Users\<user>\AppData\Roaming\images-upload-cli\.env`
