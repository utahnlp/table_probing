#!/bin/bash

# check if infotabs directory exists
if [ -d "./infotabs" ]; then
    echo "Infotabs directory already exists"
else
    echo "Cloning Infotabs..."
    git clone https://github.com/infotabs/infotabs.git
    echo "Infotabs directory cloned"
fi

if [[ "$1" == "--folder" ]]; then
    echo "Take all CSV files in folder $2"
    PREFIX=$2_integrated_batch
    CSVFILE="./$2_integrated_batch.csv"
    bash scripts/integrate.sh $2 "$PREFIX.csv"
else
    PREFIX=$1
    CSVFILE="./batches/$1.csv"
fi

echo "Prefix name is $PREFIX"
echo "CSV to be processed is $CSVFILE"

bash scripts/run_processor.sh $CSVFILE $PREFIX
bash scripts/run_agreement.sh $PREFIX
