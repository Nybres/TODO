FROM ubuntu:latest
LABEL authors="Pawel"

ENTRYPOINT ["top", "-b"]