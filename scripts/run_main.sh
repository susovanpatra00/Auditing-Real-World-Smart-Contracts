
# It runs the main.py for all the solidity files and generates the output in a csv file named output.csv
#!/bin/bash

for file in *.sol
do
  output=$(python3 main.py 1 "$file" majority_unique)
  echo "$output" | tr ' ' ',' >> output.csv
done
