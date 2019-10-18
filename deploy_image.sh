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

# Verifies if the image already exists. If not, it's built in
if ! docker image ls | grep shortest_path  >/dev/null; then 
    docker image build ${BASE_PATH} --tag shortest_path;
fi

# -v guarantees that any python code changes will be considered each time the docker image starts to run without
# rebuilding it.

CSV_PATH="/usr/database/`ls database`"
# Launch shell and REST client
docker run \
    -v=${BASE_PATH}/src/:/usr/web_app/ \
    -v=${BASE_PATH}/database/:/usr/database \
    -p 5000:5000 \
    -e CSV_PATH=${CSV_PATH} \
    -ti shortest_path

# Interactive mode to execute unitary tests
#docker run \
#    -v=${BASE_PATH}/src/:/usr/web_app/ \
#    -v=${BASE_PATH}/database/:/usr/database \
#    -p 5000:5000 \
#    -e CSV_PATH=${CSV_PATH} \
#    -it shortest_path bash