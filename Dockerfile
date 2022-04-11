FROM python:2.7-stretch
RUN pip install tox

WORKDIR /opt/wp_export_parser

COPY tox.ini .

COPY setup.py .
COPY wp_export_parser ./wp_export_parser
COPY test.py .

CMD ["bash"]