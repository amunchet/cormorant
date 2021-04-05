FROM ubuntu:latest


RUN apt-get update && apt -y install \
    dos2unix \
    python3 \
    python3-pip

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/America/Chicago/etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install -y ffmpeg

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

ENTRYPOINT [ "/src/backend/entrypoint.sh" ]