# Developer notes

## Install

```shell
mkdir <a directory>
git clone https://github.com/asreview-simulation/asreview-simulation .
python3 -m venv venv
source venv/bin/activate
pip install --editable .
```

There are various sets of dependencies that you should install depending on the work you're planning to do. 

```shell
pip install --editable .[dev]
pip install --editable .[doc2vec]
pip install --editable .[sbert]
pip install --editable .[tensorflow]
```

You can combine subsets of these into one command like so, e.g.:

```shell
pip install --editable .[sbert,doc2vec]
```

## Linting

Linting is set up to run the following tools, all via [`pre-commit`](https://pre-commit.com/):

1. `isort`: Verify the import statements are formatted consistently throughout the code base. https://pypi.org/project/isort/
2. `black`: Format the code base in accordance to `black`'s preferences. https://pypi.org/project/black/
3. `ruff`: Format and lint the code base in accordance to `ruff`'s preferences. https://pypi.org/project/ruff/
4. `mypy`: Perform static type checking. https://pypi.org/project/mypy/
5. `cffconvert`: Verify that the citation information in CITATION.cff  is valid according to the Citation File Format schema. https://pypi.org/project/cffconvert/

Here's how to run pre-commit on unstaged files:

```
pip install --editable .[dev]

# all checks
pre-commit run --all-files

# run check by id, see .pre-commit-config.yaml
pre-commit run --all-files isort
```

You can set up pre-commit to run as a git hook. In typical usage, `pre-commit` is then triggered whenever
you do a `git commit`. Enable this behavior as follows:

```shell
pre-commit install
```

## Testing

There are various types of test:
1. api tests
2. unit tests
3. tests that use mocking
4. integration tests
5. use case tests
6. tests for maintainers

Each has its own subdirectory. The tests can be run locally with:

```shell
pip install --editable .[dev]

# run all types of test
pytest

# run tests from specific directories only, e.g.
pytest tests/api tests/unit
```

Tests pertaining to a specific model have been marked accordingly with the following markers (see also `pytest`
configuration section in `pyproject.toml` or run `pytest --markers`):

| prior sampling   | feature extractor    | classifier       | querier           | balancer          | stopping   | objective function |
|------------------|----------------------|------------------|-------------------|-------------------|------------|--------------------|
| `sam_handpicked` | `fex_doc2vec`        | `clr_logistic`   | `qry_cluster`     | `bal_double`      | `stp_none` | `ofn_none`         |
| `sam_random`     | `fex_embeding_idf`   | `clr_lstm_base`  | `qry_max`         | `bal_simple`      | `stp_nq`   | `ofn_wss`          |
|                  | `fex_embedding_lstm` | `clr_lstm_pool`  | `qry_max_random`  | `bal_undersample` | `stp_rel`  |                    |
|                  | `fex_sbert`          | `clr_nb`         | `qry_uncertainty` |                   |            |                    |
|                  | `fex_tfidf`          | `clr_nn_2_layer` | `qry_random`      |                   |            |                    |
|                  |                      | `clr_rf`         | `qry_uncertainty` |                   |            |                    |
|                  |                      | `clr_svm`        |                   |                   |            |                    |

You can instruct `pytest` to run only the tests for one or some of these marked sets. As an example, if you want to run
only the tests related to Naive Bayes, you should call `pytest` with the `-m` flag as follows:

```shell
pytest -m clr_nb
```

Markers can also be combined with `or` and `and` and `not`, e.g.

```shell
pytest -m 'clr_nb and fex_tfidf'
pytest -m 'clr_rf and not fex_embedding_idf and not fex_embedding_lstm'
pytest -m 'clr_logistic or clr_rf'
# etc
```

Besides running locally, they can also be run on GitHub infrastructure by manually triggering the GitHub Action
workflow `testing`. The workflow tests whether the tests pass for all combinations of operating
system (Windows, Linux, MacOS), asreview version (1.0.4, 1.1.1, 1.2.1), and python version (3.8, 3.9, 3.10, 3.11).

Currently, the `testing` workflow on GitHub skips any tests that require TensorFlow on Python >= 3.11 (tests marked
with `clr_lstm_base`, `clr_lstm_pool`, `clr_nn_2_layer`), because `asreview` has a problem installing TensorFlow on
Python 3.11 and up.

### `tests/unit`

These tests are simple, quick to run, and mostly focus on whether the `asreview-simulation` subcommands manipulate the
state (`obj`) in the correct way. The idea of the "unit" in unit testing is that when the test fails, there is just one
thing that could have gone wrong. This is in contrast to other types of test, e.g. integration testing (see below).

### `tests/api`

These tests help safeguard against accidentally changing the api.

### `tests/use_cases`

These tests are used to automate running some use cases.

### `tests/maintainers`

These tests are to help maintain the project. At the moment, there is just one test file that safeguards the
consistency of the version string used throughout the repository.

### `tests/mocked`

The mocked tests verify whether the arguments that `SimulateReview` receives inside `asreview`'s `SimulateEntrypoint`
are the same arguments as what `SimulateReview` in `asreview_simulate` receives. The simulation inside these tests just
do the setting up of a simulation, including creating some files in a temporary directory, but they do not run. This
makes them faster than the integration tests (see below), but naturally, the simulation does not generate output files,
so there are no results to compare.

### `tests/it`

These are the most extensive type of tests. They set up a simulation using `asreview simulate`, then set up the same
simulation using `asreview simulation [subcommands with options] start`, then compare the resulting files that are
generated inside the `.asreview` file (`project.json`, `data/<dataset>.csv`, `reviews/<id>/results.sql`, and
`reviews/<id>/settings_metadata.json`, but not `feature_matrices/<extractor-method>_feature_matrix.npz` at the moment).

## Static analysis and coverage calculation

The project has been set up to use [SonarCloud](https://sonarcloud.io) to perform static analysis on the code base via
a GitHub Action named `sonarcloud`. The analysis runs on a weekly schedule but can also be triggered manually.
The results can be inspected at SonarCloud: https://sonarcloud.io/summary/overall?id=asreview-simulation. The same GitHub
Action also calculates code coverage and uploads the results to SonarCloud:
https://sonarcloud.io/component_measures?id=asreview-simulation&metric=coverage&view=list.

In addition to the GitHub Action, unit test coverage can be calculated and reported locally using:

```shell
# collect the data:
coverage run --branch --source=asreviewcontrib.simulation -m pytest tests/unit/

# print a report in the terminal:
coverage report

# write an html report to ./html
coverage html --directory=./html
```

## Generating API documentation

The project uses code comments compliant with Google Docstrings
(https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) to document its API.

HTML documentation may be generated from these code comments using the `pdoc` command line tool,
as follows:

```shell
# install dev dependencies, notably pdoc
pip install --editable .[dev]

# use pdoc to generate api docs for module asreviewcontrib.simulation.api and put it in ./docs
pdoc --docformat google -o docs asreviewcontrib.simulation.api
```

A GitHub Action named `apidocs` has been configured to generate the API documentation and host it
on GitHub Pages https://asreview-simulation.github.io/asreview-simulation.

## Packaging for distribution

```shell
pip install --editable .[dev]

# build a source distribution and put it in ./dist
python3 -m build --sdist .

# build a built distribution (a.k.a. a "wheel") and put it in ./dist
python3 -m build --wheel .
```

## Publishing: Preparation

```shell
pip install --editable .[dev]
```

Verify that

1. unit tests pass
2. api tests pass
3. use cases tests pass
4. mocked tests pass
5. integration tests pass
6. citation metadata is up to date
7. version is consistent across the repository
8. source dist can be built
9. wheel dist can be built
10. software works as expected when installing from distributable 

## Publishing: Zenodo

The repository has a GitHub action `zenodraft.yml` which can be triggered manually to publish a snapshot
of the current repository contents (`main` branch) to Zenodo as a zipped archive. The workflow does not
finalize the resulting deposition on Zenodo, so that the repository admin has a chance to review the draft
deposition before making it final by pressing the "Publish" button on Zenodo.

## Publishing: GitHub

Click the "Draft a new release" button on the releases page
[https://github.com/asreview-simulation/asreview-simulation/releases](https://github.com/asreview-simulation/asreview-simulation/releases).
Making a release is not set up to also trigger the `zenodraft` workflow.

## Known problems

1. Some models generate `results.sql` non-deterministically, making it difficult to test whether they are (still) doing
the right thing (`clr-lstm-base`, `clr-lstm-pool`, `clr-nn-2-layer`, `clr-rf`). As a workaround, the tests for these
classifiers do not compare the contents of `reviews/<review_id>/results.sql` at the moment.
2. Embedding file doesn't seem to get used during `asreview simulate`, so there is nothing to compare to
for `asreview simulation start`.

## Plugins

`asreview-simulation`'s functionality can be extended by plugins, via entry point group
`"asreview_simulationcontrib.quads"`. Items from this entry point group are expected to
be instances of
[`asreviewcontrib.simulation.api.extending.PluginQuad`](https://asreview-simulation.github.io/asreview-simulation/asreviewcontrib/simulation/api/extending.html#PluginQuad).
The sibling repository https://github.com/asreview-simulation/asreview-simulation-my-plugin provides
example plugin implementations of each model flavor.
