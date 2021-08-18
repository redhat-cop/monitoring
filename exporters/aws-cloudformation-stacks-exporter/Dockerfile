FROM registry.access.redhat.com/ubi8/python-38

# Add application sources with correct permissions for OpenShift
USER 0
# Install the dependencies
RUN pip install --upgrade pip && \
    pip install prometheus-client boto3 python-benedict
ADD aws_cfs_exporter.py .
ADD aws-stack-states.cnf .
RUN chown -R 1001:0 ./
RUN chmod 700 ./aws_cfs_exporter.py
USER 1001
EXPOSE 8000


# Run the application
# CMD ./aws_cfs_exporter.py
