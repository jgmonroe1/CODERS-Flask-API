#specifying our base image
FROM tiangolo/uwsgi-nginx-flask:python3.8

#set a directory for the app
WORKDIR /usr/src/app

#copy all the files to the container
COPY . .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#specify is the port number that needs to be exposed
EXPOSE 5000

#write the command for running the application
CMD ["python", "./app.py"]