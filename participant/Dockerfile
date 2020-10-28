FROM python:3
ENV PYTHONUNBUFFERED 1

# WorkDir inside container
RUN mkdir /code
WORKDIR /code

# Install requirements
COPY requirements.txt /code/
RUN pip install requests --user
RUN pip install influxdb --user
RUN pip install -r requirements.txt
RUN pip install djangorestframework

# Get code
COPY . /code/

#Execute
CMD ["python", "manage.py", "runserver", "0.0.0.0:8181"]
