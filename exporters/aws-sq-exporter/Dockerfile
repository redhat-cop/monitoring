FROM centos:7
RUN yum update -y ; \
    groupadd -r exporter && useradd --no-log-init -r -g exporter exporter; \
    yum install -y python-pip3 unzip python3 ;\
    pip3 install prometheus-client ; \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" ;\
    unzip awscliv2.zip ; \
    ./aws/install ; \
    rm -f ./awscliv2.zip
COPY sq_exporter.py /home/exporter/
ENV HOME=/home/exporter
EXPOSE 8999
USER exporter
CMD /home/exporter/sq_exporter.py