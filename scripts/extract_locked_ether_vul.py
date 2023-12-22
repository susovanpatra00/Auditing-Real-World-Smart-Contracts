# This script reads all the results(.txt) of smartcheck and extracts only the vulnerabilities
#      for locked_ether and stores the severity and line no. in a csv file   

import os
import csv

# Create a list to store the results
results = []

# Iterate through all text files in the current directory
for filename in os.listdir():
    if filename.endswith('.txt'):
        print(f'Parsing {filename}...')
        with open(filename) as f:
            # Read the content of the file
            content = f.read()
            
            # Split the content by new lines to get each rule as a separate string
            rules = content.split('\n\n')
            
            # Iterate through each rule to find the one with ruleId = 'SOLIDITY_LOCKED_MONEY'
            for rule in rules:
                # Extract the rule components
                components = rule.split('\n')
                rule_id = None
                severity = None
                line = None
                for c in components:
                    if 'ruleId' in c:
                        rule_id = c.split(': ')[1].strip()
                    elif 'severity' in c:
                        severity = c.split(': ')[1].strip()
                    elif 'line' in c:
                        line = c.split(': ')[1].strip()
                    if rule_id and severity and line:
                        break
                
                # Check if the ruleId matches 'SOLIDITY_LOCKED_MONEY'
                if rule_id == 'SOLIDITY_LOCKED_MONEY':
                    # Append the results to the list
                    results.append((filename, severity, line))

# Write the results to a CSV file
with open('output_le.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Filename', 'Severity', 'Line'])
    writer.writerows(results)

print('Done! Output saved to output_le.csv.')
