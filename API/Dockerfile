FROM python:3
ENV PYTHONUNBUFFERED 1

# WorkDir inside container
RUN mkdir /code
WORKDIR /code

# install requirements
COPY requirements.txt /code/
RUN pip install pika --user
RUN pip install requests --user
RUN pip install influxdb --user
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary --user

# get code
COPY . /code/

# Execute
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
