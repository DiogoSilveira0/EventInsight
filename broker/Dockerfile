FROM python:3

# WorkDir inside container
RUN mkdir /code
WORKDIR /code

# Install requirements
RUN pip install pika --user
RUN pip install influxdb --user
RUN pip install psycopg2-binary --user

ENV PYTHONUNBUFFERED=1

# Get code
COPY . /code/

# Execute
CMD ["python", "./consumer.py"]
