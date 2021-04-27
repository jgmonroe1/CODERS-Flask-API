#specify image
FROM tiangolo/uwsgi-nginx-flask:python3.8

#Copy requirements over to new dir
COPY ./requirements.txt /coders_api/requirements.txt

#copy files to container
COPY ./app /app

#install dependencies
RUN pip install -r /coders_api/requirements.txt
