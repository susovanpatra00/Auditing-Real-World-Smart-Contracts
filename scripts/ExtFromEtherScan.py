
## Code reference @sujeetc

## Import all necessary libraries
## ------------------------------

import requests
from os.path import join, splitext
import multiprocessing as mp
import json
import pandas as pd
import time
import os
import sys

## ------------------------------



## Assign api keys and paths for csv_file, reporting directory
## -----------------------------------------------------------

csv_address_file='/Users/susovanpatra/Desktop/Blockchain/Top_500/top_500_contracts.csv'
report_dir = '/Users/susovanpatra/Desktop/Blockchain/Top_500/json'
keys = ['TEZPYKHJJ3NY9TVZJTZ85BXRXWSDI44647','ZYAJP9NRF4EN6QNWHJUC8E2ESCF2HNH1F5','N3666XS9ZHAZ59KWAT19FBJRIX86ICJ6DK']
# Get API Keys from https://etherscan.io

## -----------------------------------------------------------
present_dir = os.getcwd()


## Function for ether Download api
## -------------------------------
def etherDownloadApi(file_path, action, module, add, key):
    url = 'https://api.etherscan.io/api?module=' + module + '&action=' + action + '&address=' + add + '&apikey=' + key
    # params = {'apikey': key, 'module': module, 'action': action, 'address':add}
    # # try:
    response = requests.get(url)
    print(add)
    if response.status_code == 200:
        data = response.json()
        with open(file_path, 'w') as f:
            json.dump(data, f)

## -------------------------------



## Class for counting all the parameters
## -------------------------------------

class CheckCount:

    def __init__(self):
        self.totalFiles = 0
        self.completed = 0

    def incCount(self):
        self.totalFiles += 1

    def getTotal(self):
        return self.totalFiles

    def completedCallback(self, res=''):
        self.completed += 1
        print(self.completed, " files Completed out of ", self.totalFiles)

## -------------------------------------




## Function for Downloading json files for the contract addresses
## --------------------------------------------------------------

def extractFromEthereum():
    pool = mp.Pool(10) # X keys, calls per second = 5, roughly X*3=Y works here
    df = pd.read_csv(csv_address_file)
    hashes = df["Contract_Address"].tolist()
    ProcessingResults = []
    countObj = CheckCount()
    for i in range(len(hashes)):
        contPath = join(report_dir, hashes[i]+ "_ext.json")
        ProcessingResults = pool.apply_async(etherDownloadApi, args=(contPath, 'getsourcecode', 'contract', hashes[i], keys[countObj.getTotal() % len(keys)]), callback=countObj.completedCallback)
        countObj.incCount()

    pool.close()
    pool.join()

## --------------------------------------------------------------



## Calling the function extractFromEthereum()
## ------------------------------------------

if __name__ == '__main__':
    extractFromEthereum()

## ------------------------------------------

