FROM python:3.6-slim
WORKDIR /code
ADD requirements.txt /code
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /code

