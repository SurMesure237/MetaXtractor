# asreview-simulation

Command line interface to simulate an [ASReview](https://pypi.org/project/asreview) analysis using a variety
of prior sampling strategies, classifiers, feature extractors, queriers, balancers, and stopping rules, all of which can
be configured to run with custom parameterizations.

## Status

| Badge &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;                                                                                                                                                                                       | Description                                                                                                               |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8042547.svg)](https://doi.org/10.5281/zenodo.8042547)                                                                                                                                                | Persistent identifier for archived snapshots of the software                                                              |
| [![linting](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/linting.yml/badge.svg)](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/linting.yml)                                               | Linting (`isort`,  `black`, and `ruff`, `mypy`, `cffconvert`, via `pre-commit`)                                           |
| [![testing](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/testing.yml/badge.svg)](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/testing.yml)                                               | Unit tests, mocked tests, and integration tests on combinations of operating system, ASReview version, and Python version |
| [![apidocs](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/apidocs.yml/badge.svg)](https://github.com/asreview-simulation/asreview-simulation/actions/workflows/apidocs.yml)                                               | API docs https://asreview-simulation.github.io/asreview-simulation                                                        |
| [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=asreview-simulation&metric=code_smells)](https://sonarcloud.io/summary/overall?id=asreview-simulation)                                                                          | Static code analysis report                                                                                               |
| [![Code coverage](https://sonarcloud.io/api/project_badges/measure?project=asreview-simulation&metric=coverage)](https://sonarcloud.io/summary/overall?id=asreview-simulation)                                                                           | Code coverage report                                                                                                      |
| [![GitHub release (with filter)](https://img.shields.io/github/v/release/asreview-simulation/asreview-simulation)](https://github.com/asreview-simulation/asreview-simulation/tree/0.4.0)                                                                | Link to repository state at latest GitHub release                                                                         |
| [![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/asreview-simulation/asreview-simulation/0.4.0)](https://github.com/asreview-simulation/asreview-simulation/compare/0.4.0...HEAD)  | How many commits there have been since the latest GitHub release                                                          |

## Install

```text
# generate a virtual environment
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install asreview-simulation and its dependencies
pip install git+https://github.com/asreview-simulation/asreview-simulation.git@0.4.0

# or, if you need optional dependencies as well, e.g. 'doc2vec'
pip install asreview-simulation[doc2vec]@git+https://github.com/asreview-simulation/asreview-simulation.git@0.4.0
```

## Command line interface (CLI)

Print the help:

```text
asreview simulation --help
```

Print the configuration:

```text
asreview simulation print-settings
```

With pretty-printing:

```text
asreview simulation print-settings --pretty
```

Start a simulation using the default combination of models (`sam-random`,
`bal-double`, `clr-nb`, `fex-tfidf`, `qry-max`, `stp-min`), each using its default
parameterization:

```text
asreview simulation start --benchmark benchmark:van_de_Schoot_2017 --out ./project.asreview
```

Instead of a benchmark dataset, you can also supply your own data via the `--in` option, as follows:

```text
asreview simulation start --in ./myfile.csv --out ./project.asreview
asreview simulation start --in ./myfile.ris --out ./project.asreview
asreview simulation start --in ./myfile.tsv --out ./project.asreview
asreview simulation start --in ./myfile.xlsx --out ./project.asreview
```

Using a different classifier strategy can be accomplished by using one of
the `clr-*` subcommands before issuing the `start` subcommand, e.g.:

```text
asreview simulation \
    clr-logistic \
    start --benchmark benchmark:van_de_Schoot_2017 --out ./project.asreview
```

Subcommands can be chained together, for example using the logistic
classifier with the undersample balancer goes like this:

```text
asreview simulation \
    clr-logistic \
    bal-undersample \
    start --benchmark benchmark:van_de_Schoot_2017 --out ./project.asreview
```

Most subcommands have their own parameterization. Check the help of a
subcommand with `--help` or `-h` for short, e.g.:

```text
asreview simulation clr-logistic --help
```
The above command will print:

```text
Usage: asreview simulation clr-logistic [OPTIONS]

  Configure the simulation to use Logistic Regression classifier.

Options:
  --c FLOAT             Parameter inverse to the regularization strength of
                        the model.  [default: 1.0]
  --class_weight FLOAT  Class weight of the inclusions.  [default: 1.0]
  -f, --force           Force setting the querier configuration, even if that
                        means overwriting a previous configuration.
  -h, --help            Show this message and exit.

  This command is chainable with other commands. Chained commands are
  evaluated left to right; make sure to end the chain with the 'start'
  command, otherwise it may appear like nothing is happening.

  Please report any issues at:

  https://github.com/asreview-simulation/asreview-simulation/issues.
```

Passing parameters to a subcommand goes like this:

```text
asreview simulation \
    clr-logistic --class_weight 1.1 \
    start --benchmark benchmark:van_de_Schoot_2017 --out ./project.asreview
```

By using individually parameterized, chained subcommands we can compose a
variety of configurations, e.g.:

```text
asreview simulation \
    sam-random --n_included 10 --n_excluded 15            \
    fex-tfidf --ngram_max 2                               \
    clr-nb --alpha 3.823                                  \
    qry-max-random --fraction_max 0.90 --n_instances 10   \
    bal-double --a 2.156 --alpha 0.95 --b 0.79 --beta 1.1 \
    stp-nq --n_queries 20                                 \
    start --benchmark benchmark:van_de_Schoot_2017 --out ./project.asreview
```

Chained commands are evaluated left to right; make sure to end the chain
with the `start` command, otherwise it may appear like nothing is happening.

Here is the list of subcommands:

```text
start                  Start the simulation
print-benchmark-names  Print benchmark names
print-settings         Print settings
save-settings          Save settings
load-settings          Load settings
sam-handpicked         Handpicked prior sampler
sam-random             Random prior sampler
fex-doc2vec            Doc2Vec extractor
fex-embedding-idf      Embedding IDF extractor
fex-embedding-lstm     Embedding LSTM extractor
fex-sbert              SBERT extractor
fex-tfidf              TF-IDF extractor
clr-logistic           Logistic Regression classifier
clr-lstm-base          LSTM Base classifier
clr-lstm-pool          LSTM Pool classifier
clr-nb                 Naive Bayes classifier
clr-nn-2-layer         2-layer Neural Net classifier
clr-rf                 Random Forest classifier
clr-svm                Support Vector Machine classifier
qry-cluster            Cluster query strategy
qry-max                Max query strategy
qry-max-random         Mixed query strategy (Max and Random)
qry-max-uncertainty    Mixed query strategy (Max and Uncertainty)
qry-random             Random query strategy
qry-uncertainty        Uncertainty query strategy
bal-double             Double balancer
bal-simple             No balancer
bal-undersample        Undersample balancer
stp-none               No stopping rule
stp-nq                 Stop after a predefined number of queries
stp-rel                Stop once all the relevant records have been found
ofn-none               No objective function
ofn-wss                WSS objective function
```

## Application Programming Interface (API)

For a full overview of the API, see `tests/api/test_api.py` and https://asreview-simulation.github.io/asreview-simulation. Here is an example:

```python
import os
import tempfile
from asreviewcontrib.simulation.api import Config
from asreviewcontrib.simulation.api import OneModelConfig
from asreviewcontrib.simulation.api import prep_project_directory
from asreviewcontrib.simulation.api import run


# make a classifier model config using default parameter values given the model name
clr = OneModelConfig("clr-svm")

# make a query model config using positional arguments, and a partial params dict
qry = OneModelConfig("qry-max-random", {"fraction_max": 0.90})

# make a stopping model config using keyword arguments
stp = OneModelConfig(abbr="stp-nq", params={"n_queries": 10})

# construct an all model config from one model configs -- implicitly use default model choice
# and parameterization for models not included as argument (i.e. sam, fex, bal, ofn)
config = Config(clr=clr, qry=qry, stp=stp)

# arbitrarily pick a benchmark dataset
benchmark = "benchmark:Cohen_2006_ADHD"

# create a temporary directory and start the simulation
tmpdir = tempfile.mkdtemp(prefix="asreview-simulation.", dir=".")
output_file = f"{tmpdir}{os.sep}project.asreview"
project, as_data = prep_project_directory(benchmark=benchmark, output_file=output_file)
run(config, project, as_data)
```

For more examples, refer to `tests/use_cases/test_use_cases.py`.
