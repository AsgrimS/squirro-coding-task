# Text summarizer REST API coding task for squirro

## Overview
This is a simple REST API build with [FastAPI](https://fastapi.tiangolo.com) and [MongoDB](https://www.mongodb.com/). The whole application is dockerized and runs with docker-compose.

It is capable of storing, retrieving and deleting simple text documents. It also provides a summarization endpoint that returns a summary of a given document using [Spacy](https://spacy.io/) `en_core_web_sm` nlp pipeline.

**WARNING: Use only documents written in English.**

## Quick start
1. Copy this repository to your local machine and navigate to the repository folder.
2. Using `template.env` as a template, create a new file in the base directory called `.env` and fill in the required values.
3. Run `make install` to build api docker image and install dependencies.
4. Run `make run` to start the api web server. (You can also run `make attach` to attach to the running container to see the output.)
5. Run `make clean` To stop and remove all containers and volumes.

## Make commands overview:
- `make install` - Build the docker image and install dependencies.
- `make run` - Run the api web server in detached mode.
- `make attach` - Attach to the running API container to see the FastAPI output.
- `make shell` - Attach to the running API container and open an interactive shell.
- `make stop` - Stop the running API and MongoDB containers.
- `make clean` - Stop the running API and MongoDB containers and remove them along with the volumes **(WARNING: deletes MongoDB data)**.
- `make add_dependency` - Add a new project dependency. Takes in a `name` argument. Example: `make add_dependency name=numpy`
- `make add_dev_dependency` - Add a new project development dependency. Takes in a `name` argument. Example: `make add_dev_dependency name=black`
- `make remove_dependency` - Remove a project dependency. Takes in a `name` argument. Example: `make remove_dependency name=numpy`
- `make lint` - Run black, flake8 and isort to autofix code.
- `make lint_check` - Run black, flake8, flake8-isort to check code for linting errors. Used by the pre-commit hook.