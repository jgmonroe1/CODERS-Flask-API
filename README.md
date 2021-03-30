# CODERS-Flask-API
CODERS is an open-source database project developed by the Sustainable Energy Systems Integration and Transition Group (SESIT). The focus of the SESIT Group, to develop and apply models to better understand the sustainable energy transition. The API was developed using the Python Flask framework and its functions are limited to a select set of queries. Since the API is only meant for querying, the GET HTTP request is only method implemented within the API.

## Motivations
This is API was built to provide users with access to the Canadian Open-source Database for Electricity Research and Systems-Modelling (CODERS). CODERS is an open-source database project from the [SESIT](https://sesit.cive.uvic.ca/ "SESIT Homepage") group which is resposible for many projects related Canadian electrical systems modelling. Their overall goal is helping Canada progress towards sustainable energy systems.

## Installation
The CODERS API is built with Flask, Documented with Swagger UI, Packaged with Docker, and stored here on GitHub.

### Clone Repo
Press the green "code" button and clone the repo either by:
1) Copying HTTPS URL and opening GitHub Desktop -> File -> Clone repository -> URL -> paste URL and choose location
2) Copying HTTPS URL and opening your preffered terminal -> cd into location -> run `$ git clone <URL>`
3) Press Download Zip -> find .zip file -> extract it and place in preffered location

### Build Docker Image
cd to the repos directory, then run this command:<br />
<br />
`$ docker build -t <docker_username>/coders_api .` <br />
<br />
(the period is intentional)

### Run Docker Container
While in the same directory use:<br />
<br />
`$ docker run --rm -p 8888:5000 --name coders_api <docker_username>/coders_api` <br />
<br />
to run the API <br />
<br />
*--rm auto removes container on exit* <br />
*-p 8888:5000 publish a containers port to host* <br />
*--name coders_api gives container a nickname for easier reference* <br />

### Test Out API with Swagger UI
To see if the container and Flask API is working open your favorite web browser and type in: <br />
<br />
http://127.0.0.1:8888/docs <br />
<br />
Now the Swagger UI should pop up. Look around to familiarize with the resources availbale and use the "Try It Out" button to test a request
<br />
*notice the port difference between the URL (8888) and what the flask app says (5000), this is because of the port mapping we did in the container*<br />

### Shut it Down
To stop the API press ctrl c in the terminal to stop the Flask API and then run <br />
<br />
`$ docker stop coders_api` to stop the container<br />

### Start Again
If changes to the code are made you will have to build the docker image again before running it<br />

## Creator Info
Developed by [Dustin Aldana](https://gitlab.com/DustinAldana) and [Tristan Cusi](https://github.com/cusitristan) <br />
Lead of database project [Jakub Jurasz](https://www.researchgate.net/profile/Jakub_Jurasz2)
