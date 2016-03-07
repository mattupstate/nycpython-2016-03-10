FROM python:3.5

WORKDIR /usr/src

ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONDONTWRITEBYTECODE 1

ADD requirements.pip /usr/src/
RUN pip install -r requirements.pip && rm -rf /root/.cache/pip

ADD . /usr/src
RUN pip install .

EXPOSE 5000

ENTRYPOINT ["/usr/src/bin/entrypoint"]
