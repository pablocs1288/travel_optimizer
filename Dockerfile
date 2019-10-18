FROM python:3
MAINTAINER Pablo Calvache

WORKDIR /tmp
COPY ./requirements.txt requirements.txt
COPY ./launcher.sh launcher.sh

RUN chmod +x launcher.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Persistence Path variables
ENV CSV_PATH=/usr/database/${FILE_NAME}

# Config flask
ENV FLASK_APP "/usr/web_app/flask_instance.py"

# launching
WORKDIR /usr/web_app
CMD ["/tmp/launcher.sh", "/usr/web_app/"]
