import csv
import requests

# Etherscan API key
api_key = "DU3TWEU4QIDH3MS4ANPQ88T3KRPQA3V7RJ"

# List of contract addresses in a CSV file
contract_addresses_file = "contracts.csv"

# Output file for top 500 contracts with max ether value locked
output_file = "top_500_contracts.csv"

# Initialize an empty list to store contract addresses
contract_addresses = []

# Read contract addresses from CSV file and append to list
with open(contract_addresses_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        contract_addresses.append(row[0])

# Initialize an empty dictionary to store ether values for each contract address
contract_eth_values = {}

# Loop through each contract address and get its ether balance using Etherscan API
for i, contract_address in enumerate(contract_addresses):
    print(f"Processing contract {i+1}/{len(contract_addresses)}: {contract_address}")
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={contract_address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        ether_value = int(response.json()["result"]) / 10**18
        contract_eth_values[contract_address] = ether_value
    else:
        print(f"Failed to get ether value for contract {contract_address}")

# Sort contracts by ether value in descending order and take top 500
sorted_contracts = sorted(contract_eth_values.items(), key=lambda x: x[1], reverse=True)[:500]

# Write top 500 contracts to output file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Contract Address", "Ether Value"])
    for contract in sorted_contracts:
        writer.writerow([contract[0], contract[1]])
