FROM python:3.9
WORKDIR /usr/src/netapp_exporter
ADD . /usr/src/netapp_exporter
RUN pip install pipenv && pipenv install --system
ENTRYPOINT ["python", "src/main.py"]
EXPOSE 9418
