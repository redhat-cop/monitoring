FROM python:3.9
WORKDIR /usr/src/flex_exporter
ADD . /usr/src/flex_exporter
RUN pip install pipenv && pipenv install --system
ENTRYPOINT ["python", "src/main.py"]
EXPOSE 9417
