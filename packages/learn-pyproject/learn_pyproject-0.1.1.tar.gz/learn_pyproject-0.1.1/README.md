# learn-pyproject

Experiments with modern python project tooling.

https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
https://python-poetry.org/docs

### PyPi Project Page
http://pypi.org/project/learn-pyproject/0.1.1/

### Install Poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -
poetry completions bash >> ~/.bashrc
echo "source /etc/bash_completion" >> ~/.bashrc
poetry --version
```

### [Basic Usage](https://python-poetry.org/docs/basic-usage/)

```sh
# create venv and install dependencies
poetry install
# activate venv
$(poetry env activate)
# list all venvs
poetry env list
# delete the current venv (and all installed dependencies)
poetry env remove $(poetry env list | grep Activated | awk '{ print $1 }')
# alternatively, use `poetry run` which will use the venv
poetry run python src/learn_pyproject/hello.py
```

### [Managing Dependencies](https://python-poetry.org/docs/managing-dependencies/)

```sh
# discard lockfile and resolve dependencies again
poetry update
# fix lockfile
poetry lock
# make sure only the dependencies in the lockfile are installed
poetry sync
# add dependencies
poetry add requests
# add optional dependencies in a group
poetry add pytest --group test
# install the optional group dependencies
poetry install --with test
# exclude optional dependencies
poetry install --without test,docs
# explicitly select groups to install
poetry install --only main # runtime deps are implicitly named main
poetry show --tree
poetry show --all
```

### [Libraries](https://python-poetry.org/docs/libraries/)

```sh
poetry build # sdist (source, .tar.gz), wheel (compiled, .whl)

poetry publish # requires .pypirc credentials, see https://python-poetry.org/docs/repositories/#configuring-credentials
poetry config pypi-token.pypi <token>
poetry publish --build # note published versions are immutable. You have to change the version number to publish again. Use semver.
```

### [Commands](https://python-poetry.org/docs/cli/)