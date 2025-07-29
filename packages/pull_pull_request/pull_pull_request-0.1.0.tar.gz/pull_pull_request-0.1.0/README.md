# pull_pull_request

[![pypi](https://img.shields.io/pypi/v/pull_pull_request.svg)](https://pypi.python.org/pypi/pull_pull_request)
[![license](https://img.shields.io/github/license/samuelcolvin/pull_pull_request.svg)](https://github.com/samuelcolvin/pull_pull_request/blob/main/LICENSE)

CLI for pull from pull requests and pushing to them.

## Installation

```bash
uv tool install pull_pull_request
```

Add the an alias to your `~/.gitconfig`:

```toml
[alias]
    ppr = "!f() { pull_pull_request $@; }; f"
    ...
```

## Usage

To pull:

```bash
git ppr <pull request id>
```

To push back to that branch:

```bash
git ppr <pull request id> push
```
