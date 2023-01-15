#!/bin/sh 

# This script will automate the starting and running of the flask server and python virtual enviroment venv
# Written by: Ayushmaan Aggarwal

# Move to right directory
echo "Starting Script"
cd /home/ayu/theAnishCounter

echo && echo 

# Pull existing changes
echo "Pulling changes from live branch"
git checkout live
git pull 

echo && echo 

# Start virtual enviroment
echo "Activate python virtual enviroment"
source venv/bin/activate

echo && echo 

# Install missing packages
echo "Installing missing python packages"
pip install -r requirements.txt

echo && echo 

# Run flask server 
# (python file is run.py and app is the app variable)
# echo "Running flask server"
# ./venv/bin/gunicorn -w 9 main:app

# instead of running above command, the server will be 
# using supervisor: # sudo supervisorctl reload