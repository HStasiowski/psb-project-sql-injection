FROM postgres:latest
LABEL authors="HStasiowski"

WORKDIR /usr/src/app
RUN mkdir -p /data/dbs
RUN chown postgres /data/dbs
COPY psb_project/dellstore2/dellstore2-normal-1.0.sql /usr/src/app/
COPY psb_project/dellstore2/setup_db.sql /usr/src/app/
