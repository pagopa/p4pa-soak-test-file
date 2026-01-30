# p4pa-soak-test-file
A repository designed to generate and import files on Piattaforma Unitaria.

## Installation
Install [pipenv](https://pipenv.pypa.io/en/latest/):

```
pip install pipenv
```

Create and enter the virtual environment:

```commandline
pipenv shell
```

Install dependencies:

```commandline
pipenv sync
```

Update dependencies:
```commandline
pipenv run pip freeze > requirements.txt
pipenv install -r requirements.txt
```

> **_NOTE_**: Create `pu_feature_secrets.yaml` based on `pu_feature_secrets_template.yaml` and customize it.

## Test execution
Execute the script `run.sh` provided in order to run it.
See its help function to know more about the parameters it accepts.
