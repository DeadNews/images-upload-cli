# Changelog

## [3.1.0-alpha.7](https://github.com/DeadNews/images-upload-cli/compare/v3.0.2...v3.1.0-alpha.7) - 2024-04-08

### 🚀 Features

- replace `pyperclip` with `copykitten` - ([d5b760b](https://github.com/DeadNews/images-upload-cli/commit/d5b760b2770a16f00d434db893bb241758397057))
- replace `pyperclip` with `copykitten` - ([8429e12](https://github.com/DeadNews/images-upload-cli/commit/8429e12147d9b58b8bdb8febd164ad4beb256db9))

### 📚 Documentation

- _(changelog)_ update `git-cliff` config - ([1b7f60b](https://github.com/DeadNews/images-upload-cli/commit/1b7f60bbe0c171ee5f9468bdff82b3708bcd6c48))
- _(mkdocs)_ add `navigation.instant` - ([445a4ca](https://github.com/DeadNews/images-upload-cli/commit/445a4ca6cac7473afb4cdc8629b4d447c67887a2))
- _(readme)_ update badges - ([ed78a01](https://github.com/DeadNews/images-upload-cli/commit/ed78a01164aad3f1078b4043524d164a2743150c))

### 🧹 Chores

- _(makefile)_ update `release` command - ([c4ca3a0](https://github.com/DeadNews/images-upload-cli/commit/c4ca3a04eaef1607dc350bf2f0d1bc8ee9f66ad1))

### ⚙️ CI/CD

- _(github)_ update `pypi-deploy` job - ([9d5ba92](https://github.com/DeadNews/images-upload-cli/commit/9d5ba9226bdb0d62fe12908f10067d49217d1334))
- _(github)_ update `build-win` job ([#197](https://github.com/DeadNews/images-upload-cli/issues/197)) - ([d1eedc7](https://github.com/DeadNews/images-upload-cli/commit/d1eedc72f1d9d3701935568526b34134c2d381d8))
- _(github)_ update aur release job ([#196](https://github.com/DeadNews/images-upload-cli/issues/196)) - ([4e2e87c](https://github.com/DeadNews/images-upload-cli/commit/4e2e87c8564dced1c3bd61da1c1274c7643edd1a))

### ◀️ Revert

- 'feat: replace `pyperclip` with `copykitten`' - ([1e0c66f](https://github.com/DeadNews/images-upload-cli/commit/1e0c66f636388b30eb4773913c4b855764ef5a38))

## [3.0.2](https://github.com/DeadNews/images-upload-cli/compare/v3.0.1...v3.0.2) - 2024-04-03

### 🐛 Bug fixes

- update deprecated name for `pillow 10.3.0` compatibility ([#189](https://github.com/DeadNews/images-upload-cli/issues/189)) - ([c0c5897](https://github.com/DeadNews/images-upload-cli/commit/c0c5897ad27c22c80ee7e2e7dbe7a6eaf6f3f4b5))

### 📚 Documentation

- _(changelog)_ add `git-cliff` ([#186](https://github.com/DeadNews/images-upload-cli/issues/186)) - ([64b44d4](https://github.com/DeadNews/images-upload-cli/commit/64b44d4cb1baa36679c6708702dfc63810385e14))
- _(mkdocs)_ add ([#184](https://github.com/DeadNews/images-upload-cli/issues/184)) - ([cd2fbf0](https://github.com/DeadNews/images-upload-cli/commit/cd2fbf0cd8de48db713c89dbd43c11d6a9400896))
- _(readme)_ add badges - ([8912d71](https://github.com/DeadNews/images-upload-cli/commit/8912d71b9a2a60090f072d666901e0b7abcd5144))

### 🧹 Chores

- update linting tasks in `makefile` and `poe` - ([e01404a](https://github.com/DeadNews/images-upload-cli/commit/e01404aad59b559f7d148fa3fed520b2e4a78942))

### ⬆️ Dependencies

- _(deps)_ update dependency pillow to v10.3.0 ([#190](https://github.com/DeadNews/images-upload-cli/issues/190)) - ([df49044](https://github.com/DeadNews/images-upload-cli/commit/df490441833f37ac17777e984015f9af4245c6e8))
- _(deps)_ update dependency rich to v13.7.1 ([#179](https://github.com/DeadNews/images-upload-cli/issues/179)) - ([9191acc](https://github.com/DeadNews/images-upload-cli/commit/9191acca8ff27f32e16afc4ae38360f73a9644ca))

## [3.0.1](https://github.com/DeadNews/images-upload-cli/compare/v2.0.1...v3.0.1) - 2024-02-22

### 🚀 Features

- add logger and error handling ([#175](https://github.com/DeadNews/images-upload-cli/issues/175)) - ([15678ee](https://github.com/DeadNews/images-upload-cli/commit/15678ee29bb848663d093407405bb496c85a4759))
- add `anhmoe` image hosting ([#174](https://github.com/DeadNews/images-upload-cli/issues/174)) - ([c1f401b](https://github.com/DeadNews/images-upload-cli/commit/c1f401b8f0e9d7dda089a912d8f4cacd03a54864))
- update public accessible objects of that module ([#171](https://github.com/DeadNews/images-upload-cli/issues/171)) - ([99b81de](https://github.com/DeadNews/images-upload-cli/commit/99b81de5e9bb7d31a2301908c4de44de17789ba2))

### 🐛 Bug fixes

- [**breaking**] remove the `-c/-C` shortcut from the `clipboard` cli option ([#177](https://github.com/DeadNews/images-upload-cli/issues/177)) - ([0aafcce](https://github.com/DeadNews/images-upload-cli/commit/0aafcce7e63c0e5fdd35d9184b7d7bae185f4a53))

### 📚 Documentation

- update docstrings ([#176](https://github.com/DeadNews/images-upload-cli/issues/176)) - ([1f5b20d](https://github.com/DeadNews/images-upload-cli/commit/1f5b20dfa0ddf2065efbd21456fcd5a1c1f4b9a0))

### 🎨 Styling

- update `ruff` settings ([#162](https://github.com/DeadNews/images-upload-cli/issues/162)) - ([ca58de3](https://github.com/DeadNews/images-upload-cli/commit/ca58de3b98400bf586d06f03b6b55f6d7503a400))

### 🧪 Testing

- update tests ([#122](https://github.com/DeadNews/images-upload-cli/issues/122)) - ([6226443](https://github.com/DeadNews/images-upload-cli/commit/622644371147c16b5e872bdd9a06bf523cd749b4))

### 🧹 Chores

- replace `black` with `ruff` - ([46cf164](https://github.com/DeadNews/images-upload-cli/commit/46cf1644ee9e6d48b0b96305746da937a2365069))
- update docstrings ([#132](https://github.com/DeadNews/images-upload-cli/issues/132)) - ([44fe8e6](https://github.com/DeadNews/images-upload-cli/commit/44fe8e603682a4efdaccf030bfd68f56e65d55cf))
- specify python `target-version` - ([794a622](https://github.com/DeadNews/images-upload-cli/commit/794a622befd3d9c9e300057b0c8f088aa375c7b0))

### ⚙️ CI/CD

- _(pre-commit)_ add `checkmake` hook - ([85c19cb](https://github.com/DeadNews/images-upload-cli/commit/85c19cbd6b0e22cc7e5b192f62967581887c33a5))
- _(pre-commit)_ add `actionlint` hook - ([8a2ceb1](https://github.com/DeadNews/images-upload-cli/commit/8a2ceb140ffb94485a029d96f16e98b8de262e54))
- _(pre-commit)_ use `black` mirror - ([90444aa](https://github.com/DeadNews/images-upload-cli/commit/90444aa8b25c8e8b34f6c2d1db72ba934facceb4))
- build a `windows` executable using the `nuitka` compiler ([#167](https://github.com/DeadNews/images-upload-cli/issues/167)) - ([a28be07](https://github.com/DeadNews/images-upload-cli/commit/a28be079833a80cdfae5eb6bbb0d941647c5bc13))
- add `python 3.12` to tests matrix ([#138](https://github.com/DeadNews/images-upload-cli/issues/138)) - ([904be1b](https://github.com/DeadNews/images-upload-cli/commit/904be1b03d5faa6f09bb226efd655e412eaa6408))
- use `environment` for `aur` deploy - ([92df766](https://github.com/DeadNews/images-upload-cli/commit/92df76614c1860959d34f60d07903b3f258a6835))
- disable `codeql` on `schedule` - ([25fd100](https://github.com/DeadNews/images-upload-cli/commit/25fd10032f0b57c129c72bb98b19bbaf92c4ea18))

### ⬆️ Dependencies

- _(deps)_ update dependency python-dotenv to v1.0.1 ([#161](https://github.com/DeadNews/images-upload-cli/issues/161)) - ([f7f57f3](https://github.com/DeadNews/images-upload-cli/commit/f7f57f3006d81aa1fb42a365fcd97318a80d732b))
- _(deps)_ update dependencies ([#158](https://github.com/DeadNews/images-upload-cli/issues/158)) - ([ac8078d](https://github.com/DeadNews/images-upload-cli/commit/ac8078d41bfb28e33934e3d81666dbd8bb33078b))
- _(deps)_ update dependency pillow to v10.2.0 ([#157](https://github.com/DeadNews/images-upload-cli/issues/157)) - ([8073735](https://github.com/DeadNews/images-upload-cli/commit/8073735d0515ff31ca50ec50928337c3efc4f4fe))
- _(deps)_ update dependency httpx to v0.25.2 ([#148](https://github.com/DeadNews/images-upload-cli/issues/148)) - ([df8ef71](https://github.com/DeadNews/images-upload-cli/commit/df8ef7137f62f65f136d8d54219a45d4d5465749))
- _(deps)_ update dependency httpx to v0.25.1 ([#144](https://github.com/DeadNews/images-upload-cli/issues/144)) - ([12639f7](https://github.com/DeadNews/images-upload-cli/commit/12639f7d75270a1d69c8f02f8105583775231c5a))
- _(deps)_ update dependency pillow to v10.1.0 ([#143](https://github.com/DeadNews/images-upload-cli/issues/143)) - ([48ca32f](https://github.com/DeadNews/images-upload-cli/commit/48ca32fc39738d56d4746a5dc69e03f44a117a77))
- _(deps)_ update dependency pillow to v10.0.1 ([#133](https://github.com/DeadNews/images-upload-cli/issues/133)) - ([a0123a4](https://github.com/DeadNews/images-upload-cli/commit/a0123a49c055539c9d6190d417671da02d7bfb75))
- _(deps)_ update dependency click to v8.1.7 ([#127](https://github.com/DeadNews/images-upload-cli/issues/127)) - ([a5da102](https://github.com/DeadNews/images-upload-cli/commit/a5da1029c3087685464448bed15605ee6fd9d5d0))
- _(deps)_ update dependency click to v8.1.6 ([#123](https://github.com/DeadNews/images-upload-cli/issues/123)) - ([2a28aea](https://github.com/DeadNews/images-upload-cli/commit/2a28aea40fd6d4e33ad1b773cf5d60c3433940f2))
- _(deps)_ update dependency click to v8.1.5 ([#119](https://github.com/DeadNews/images-upload-cli/issues/119)) - ([ebbb719](https://github.com/DeadNews/images-upload-cli/commit/ebbb719e61b92dd3d79ecd0af4c71efe743ea922))

## [2.0.1](https://github.com/DeadNews/images-upload-cli/compare/v2.0.0...v2.0.1) - 2023-07-11

### 🚀 Features

- call `get_font` only once ([#117](https://github.com/DeadNews/images-upload-cli/issues/117)) - ([2be7eca](https://github.com/DeadNews/images-upload-cli/commit/2be7eca2a0a3fb2584be2e2f472e5b13649f9c06))

### 🧪 Testing

- rename `.env.sample` - ([73c59c5](https://github.com/DeadNews/images-upload-cli/commit/73c59c50fb1b927b071981ea1065ac14cd335fe0))

### ⬆️ Dependencies

- _(deps)_ update dependency pillow to v10 ([#113](https://github.com/DeadNews/images-upload-cli/issues/113)) - ([6bd957f](https://github.com/DeadNews/images-upload-cli/commit/6bd957f6ed7f54758c21a6631cf611d17e542efe))

## [2.0.0](https://github.com/DeadNews/images-upload-cli/compare/v1.1.3...v2.0.0) - 2023-06-24

### 🚀 Features

- simplify cli - ([c01c6c5](https://github.com/DeadNews/images-upload-cli/commit/c01c6c53db06999009bbbfda7009f81ee2d4af07))
- use `asyncio` ([#106](https://github.com/DeadNews/images-upload-cli/issues/106)) - ([d6966de](https://github.com/DeadNews/images-upload-cli/commit/d6966deac152c974a9d0e73c3674859877e76dcc))
- rename `get_env` func - ([b5fea88](https://github.com/DeadNews/images-upload-cli/commit/b5fea88d7cb929340411b25afc9d7cbbb7ebfd70))

### 📚 Documentation

- fix `workflow` name - ([1dd9115](https://github.com/DeadNews/images-upload-cli/commit/1dd91159420a93b877ab3881b5164952756ff9c4))

### 🧪 Testing

- use `pragma: no cover` ([#110](https://github.com/DeadNews/images-upload-cli/issues/110)) - ([c47567a](https://github.com/DeadNews/images-upload-cli/commit/c47567a3eccf2f17bfae1d252854b39c336d5f44))

### 🧹 Chores

- rename poetry `group` - ([98852e1](https://github.com/DeadNews/images-upload-cli/commit/98852e134d1810ed3d12cbccc7ede5ceae6c78a4))

### ⚙️ CI/CD

- _(pre-commit)_ add `typos` hook - ([892b6ce](https://github.com/DeadNews/images-upload-cli/commit/892b6cebf0c2cd047467cf6220f4d3d91266ece4))
- _(renovate)_ use shared config - ([9fe50ad](https://github.com/DeadNews/images-upload-cli/commit/9fe50ad0c2bf4fdcc69d33bb719144a0ab683dbe))
- use `digest pinning` - ([d9bc707](https://github.com/DeadNews/images-upload-cli/commit/d9bc707990478082e22c0bcc5f10d3aa2575f6f9))
- rename `deps-review` - ([aafd1fe](https://github.com/DeadNews/images-upload-cli/commit/aafd1fe60484a4ae3f6b7cd91cf68ecc8fc23c1a))
- update `workflows` ([#98](https://github.com/DeadNews/images-upload-cli/issues/98)) - ([342e77c](https://github.com/DeadNews/images-upload-cli/commit/342e77cba5d31ce778eea876ba44485f12062f6b))

### ⬆️ Dependencies

- _(deps)_ update dependency requests to v2.31.0 ([#95](https://github.com/DeadNews/images-upload-cli/issues/95)) - ([3b302dc](https://github.com/DeadNews/images-upload-cli/commit/3b302dc67172fc0e3cf62d82d37ad09204cf8e86))

## [1.1.3](https://github.com/DeadNews/images-upload-cli/compare/v1.1.1...v1.1.3) - 2023-05-08

### 👷 Build

- update `PKGBUILD` ([#86](https://github.com/DeadNews/images-upload-cli/issues/86)) - ([864d257](https://github.com/DeadNews/images-upload-cli/commit/864d257202732bdd31af81fe0c705cae5e00f3d2))

### ⚙️ CI/CD

- fix deploy to `aur` - ([571b763](https://github.com/DeadNews/images-upload-cli/commit/571b7639a01b227f82748ffb6468af88d2c9b89d))

## [1.1.1] - 2023-05-07

### 🚀 Features

- dev pr ([#77](https://github.com/DeadNews/images-upload-cli/issues/77)) - ([9b3e7a6](https://github.com/DeadNews/images-upload-cli/commit/9b3e7a68e21d343e03634eff7e1ac55b8448d276))

### 🐛 Bug fixes

- _(build)_ enable `poetry-dynamic-versioning` - ([5007861](https://github.com/DeadNews/images-upload-cli/commit/50078619083700a8f8fc0765ac05c272f08cf3a3))

### ⬆️ Dependencies

- _(deps)_ update dependency requests to v2.30.0 - ([6d3932b](https://github.com/DeadNews/images-upload-cli/commit/6d3932b28a81d9ee0db85cc1ad8e54c05376a658))

<!-- generated by git-cliff -->
