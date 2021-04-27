FROM centos:7
RUN yum update -y ; \
    groupadd -r exporter && useradd --no-log-init -r -g exporter exporter; \
    yum install -y python-pip3 unzip python3 ;\
    pip3 install prometheus-client boto3;
COPY sq_exporter.py /home/exporter/
ENV HOME=/home/exporter
EXPOSE 8999
USER exporter
CMD /home/exporter/sq_exporter.py
