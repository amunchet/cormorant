FROM ubuntu:latest

RUN apt-get update && apt -y install \
    dos2unix \
    python3 \
    python3-pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

ENTRYPOINT [ "/src/backend/entrypoint.sh" ]