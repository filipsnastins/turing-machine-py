# turing-machine-py

Turing Machine interpreter implementation in Python - Discrete math course project.

- [turing-machine-py](#turing-machine-py)
  - [Usage](#usage)
  - [Installation](#installation)
  - [Testing](#testing)
  - [Development](#development)

## Usage

The look of `turing-machine-py` programming interface has been inspired by [turingmachine.io](https://turingmachine.io/).

- To create your own Turing Machine program, import these classes from the package:

```python
from turing_machine_py import State, Instruction, TuringMachine
```

- `State` is the state of the TM that carries name and list of `Instruction`. One state can have many `Instruction`.

- `Instruction` describes what to do when TM *meets/sees* a symbol on a tape.

- `TuringMachine` is the runner class. It receives input data and list of states.

Check out examples in [tests](tests) folder - it contains few sample programs with description.


## Installation
- Choose one of suitable package installation methods

  - With [Poetry](https://python-poetry.org/)

    ```
    poetry install
    ```

  - With `pip`

    - Create virtual environment

    ```
    python -m venv .venv
    ```

    - Activate virtual environment

    ```
    .\.venv\Scripts\activate  # Windows
    source ./venv/bin/activate  # Linux
    ```

    ```
    python -m pip install -U pip setuptools wheel
    pip install -r requirements.txt
    pip install -e .
    ```

## Testing

- Run tests with `pytest`.
- Run `pytest --log-cli-level=INFO` to output every Turing Machine step to the console.

## Development

- [Pre-commit hooks](.pre-commit-config.yaml)

```
pre-commit install
```

- Helper [scripts.py](scripts.py)

```
poetry run hooks
poetry run format
poetry run lint
poetry run test
poetry run test-cov-term
poetry run test-cov-html
```

- Export requirements from Poetry

```
poetry export -f requirements.txt --dev --without-hashes
```
