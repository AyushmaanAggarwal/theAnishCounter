#!/bin/sh 

# This script will automate the starting and running of the flask server and python virtual enviroment venv
# Written by: Ayushmaan Aggarwal

# Move to right directory
cd /home/ayu/theAnishCounter

# Pull existing changes
git checkout main
git pull 

# Start virtual enviroment
source venv/bin/activate

# Install missing packages
pip install -r requirements.txt

# run flask server 
# (python file is run.py and app is the app variable)
gunicorn -w 9 run:app