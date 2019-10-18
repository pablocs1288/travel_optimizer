#!/usr/bin/env bash

BASE_PATH=`pwd`
CSV_NAME=$1

if [ -z "${CSV_NAME}" ]; then 
    echo "No csv file indicated. Breaking deployment process"; exit $rc
fi

# Removing all stored csv's
rm ${BASE_PATH}/database/*.csv
# Copying new graph/csv
cp ${CSV_NAME} ${BASE_PATH}/database/
if [[ "$?" -ne 0 ]] ; then
  echo 'Could not find the csv file. Breaking deployment process'; exit $rc
fi


export CSV_PATH=${BASE_PATH}/database/`ls database`
export FLASK_APP="src/flask_instance.py"

chmod +x launcher.sh
./launcher.sh src

