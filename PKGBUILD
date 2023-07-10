# Maintainer: DeadNews <aurczpbgr@mozmail.com>

pkgbase="python-images-upload-cli"
pkgname=("python-images-upload-cli")
_name="images_upload_cli"
pkgver="2.0.0"
pkgrel=1
pkgdesc="Upload images via APIs"
url="https://github.com/DeadNews/images-upload-cli"
depends=(
    "python"
    "python-click"
    "python-dotenv"
    "python-httpx"
    "python-pillow"
    "python-pyperclip"
)
makedepends=(
    "python-installer"
)
license=("MIT")
arch=("any")
source=("https://files.pythonhosted.org/packages/py3/${_name::1}/${_name}/${_name}-$pkgver-py3-none-any.whl")
sha256sums=("SKIP")

package() {
    python -m installer --destdir="${pkgdir}" "${_name}-$pkgver-py3-none-any.whl"
}
