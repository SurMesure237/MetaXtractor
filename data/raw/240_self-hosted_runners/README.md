# Example repo for a GitHub self-hosted runner

Contains a Python package called `justatest` and a unit test for it.

To test with your own runner

1. [Duplicate](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) this repo
2. Change visibility to private
3. Set up runner as described in [https://github.com/ci-for-research/self-hosted-runners](https://github.com/ci-for-science/self-hosted-runners)
4. Make change to repo to trigger [GitHub Action workflow](.github/workflows/ci.yml) to run.

## Install

```shell
poetry install
```

## Usage

```python
from justatest import sum
assert sum(2, 4) == 6
```

## Run tests

```shell
poetry run pytest tests
```

