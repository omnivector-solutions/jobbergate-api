FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1
ENV WORKDIR /code
ENV PATH=$PATH:/code/scripts

RUN mkdir $WORKDIR
COPY . $WORKDIR
RUN apt update -y \
    && apt install postgresql-client-common postgresql-client-11 -y \
    && pip install --no-cache-dir -r /code/requirements/requirements.txt

WORKDIR $WORKDIR
EXPOSE 8080

ENTRYPOINT ["scripts/docker-entrypoint.sh"]
