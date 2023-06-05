#! /usr/bin/bash

echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "venv" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
source venv/bin/activate
export FLASK_APP=main:dev_app
export ENV=development
# echo $(current_app)
flask --debug run
# deactivate