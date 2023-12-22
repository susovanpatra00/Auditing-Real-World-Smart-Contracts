#!/bin/bash
# This bash file is used to run the run_slither.sh for all the solidity file to create the corresponding .sol.json file

for file in *.sol
do
    bash run_slither.sh "$file"
done
