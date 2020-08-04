FROM python:3.7-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry==1.*

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Install the dependencies which are cached in this docker layer
RUN  poetry install --no-interaction --no-ansi --no-dev --no-root

COPY ./feedback_bot /code/feedback_bot
COPY ./data/replies /replies

# Build and install project with the scripts
RUN poetry install --no-interaction --no-ansi --no-dev

# Run bot inside virtual environment
# See pyproject.toml for `run_bot` cli script details
ENTRYPOINT poetry run run_bot
