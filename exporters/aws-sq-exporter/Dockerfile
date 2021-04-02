FROM registry.access.redhat.com/ubi8/python-38
# Add application sources with correct permissions for OpenShift
USER 0
ADD sq_exporter.py .
ADD metrics.yaml .
RUN chown -R 1001:0 ./
USER 1001
EXPOSE 8000
# Install the dependencies
RUN pip install --upgrade pip && \
    pip install prometheus-client boto3 python-benedict

# Run the application
CMD sq_exporter.py
