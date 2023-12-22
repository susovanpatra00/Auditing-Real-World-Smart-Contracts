
## Code reference @sujeetc

## Import all necessary libraries
## ------------------------------

from os.path import join, splitext
import json
import pandas as pd
import os

## ------------------------------



## Assign paths for csv_file, reporting directory
## -----------------------------------------------------------

csv_address_file='/Users/susovanpatra/Desktop/Blockchain/Top_500/top_500_contracts.csv'
report_dir = '/Users/susovanpatra/Desktop/Blockchain/Top_500/sol'

## -----------------------------------------------------------

present_dir = os.getcwd()



## Function for converting .json to .sol file
## ------------------------------------------

def parse_json(filename):
		with open(filename) as access_json:
			read_content = json.load(access_json)
		results = read_content['result']
		file_to_create=present_dir+"/"+filename.replace('.json','.sol')
		for result in results:
			with open(file_to_create,'w') as file:
				file.write(result['SourceCode'])

## ------------------------------------------



## Defining the attribute to fetch in csv file
## -------------------------------------------
     
df = pd.read_csv(csv_address_file)
hashes = df["Contract_Address"].tolist()

## -------------------------------------------



## Calling the parse_json function and giving address
## --------------------------------------------------

if __name__ == '__main__':
    for i in range(len(hashes)):
        parse_json("sol/"+hashes[i] + "_ext.json")
	
## --------------------------------------------------


