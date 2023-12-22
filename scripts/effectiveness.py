import csv

false_positives = 0
effective_analyses = 0
total_contracts = 0

with open('/Users/apple/Downloads/bug_report.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        slither_analysis = row['SLITHER ANALYSIS']
        if slither_analysis and int(slither_analysis) == 0:
            false_positives += 1
        elif slither_analysis and int(slither_analysis) == 1:
            effective_analyses += 1
        total_contracts += 1

print("Number of false positives:", false_positives)
print("Number of effective analyses:", effective_analyses)
print("Total number of contracts analyzed:", total_contracts)

if total_contracts > 0:
    effectiveness_percentage = effective_analyses / total_contracts * 100
    print("Effectiveness percentage:", effectiveness_percentage, "%")
else:
    print("No contracts were analyzed.")
