
FROM python:3.14


WORKDIR /home/app


COPY ./requirements.txt /code/requirements.txt
COPY ./alembic ./alembic
COPY ./db ./db
COPY ./scripts ./scripts

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]