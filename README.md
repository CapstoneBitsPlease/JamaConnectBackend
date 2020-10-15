# Jama and Jira integration
### this is the python server that will act as the bridge between Jama and Jira

## requirements
install PyJama: https://github.com/jamasoftware-ps/py-jama-rest-client

install flask:`pip3 install flask`

install the java web token library `pip3 install flask-jwt-extended`

## To run
flask can be run quite nicely from through VS Code `shft+cmd+D` will take you to the debug console. from there you will be given the option of running the code. select `python: flask app` from the list of options and set the path to server.py

see link for more information about running flask in VS Code

https://code.visualstudio.com/docs/python/tutorial-flask

make sure that you're using the correct python environment otherwise pyjama and flask wont work

contact Spencer if you are having any issues getting it running. 

## Database
the database can be directly viewed and edditied using DataGrip, just point it to the .db file.
