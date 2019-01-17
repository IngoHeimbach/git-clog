# Git colorlog

## Introduction

`git clog` outputs the commit graph of the current Git repository and colorizes commit symbols by interpreting the first
six commit hash digits as an RGB color value:

![git clog screenshot](https://raw.githubusercontent.com/IngoHeimbach/git-clog/master/screenshot.png)

**Important note**: You need a [terminal with true color support](https://gist.github.com/XVilka/8346728).

## Installation and usage

`git clog` is [available on PyPI](https://pypi.org/project/git-clog/) and can be installed with `pip`:

```bash
python3 -m pip install git-clog
```

After the installation, call

```bash
git clog
```

within a Git repository.
