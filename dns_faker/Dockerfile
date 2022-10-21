FROM python:3.10-alpine

RUN pip install dnspython

ADD ./main.py /work/main.py

WORKDIR /work

ENTRYPOINT [ "python", "-u", "main.py"]