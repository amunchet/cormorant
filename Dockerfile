FROM ubuntu:latest

RUN apt update && apt install -y python3 \
	python3-pip \
	curl  \
	wget

RUN pip3 install pytest
