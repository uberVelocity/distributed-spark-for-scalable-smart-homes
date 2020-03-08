FROM bitnami/spark:latest

COPY regression.py /opt/bitnami/spark

USER root
RUN mkdir .ivy2
RUN chown 1001:1001 .ivy2
USER 1001
