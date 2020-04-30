FROM python:3.7

COPY requirements.txt /srv

RUN pip3 install -r /srv/requirements.txt

COPY . /srv

WORKDIR /srv

EXPOSE 8080

ENTRYPOINT ["gunicorn", "-b:8080", "warc_proxy:app"]
