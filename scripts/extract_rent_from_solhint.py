import csv
import glob
import re

# create a list to store the results
results = []

# iterate over all text files in the current directory
for file_path in glob.glob("*.txt"):
    with open(file_path, "r") as file:
        # read the contents of the file
        content = file.read()

        # find all occurrences of 'ruleId: reentrancy'
        pattern = r"ruleId:\s*reentrancy\b"
        matches = re.findall(pattern, content)

        # iterate over the matches and extract the line and column numbers
        for match in matches:
            line_num = int(re.search(r"line:\s*(\d+)", content).group(1))
            col_num = int(re.search(r"column:\s*(\d+)", content).group(1))
            results.append((file_path, line_num, col_num))

# write the results to a CSV file
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["file_path", "line_num", "col_num"])
    writer.writerows(results)

print(f"Processed {len(glob.glob('*.txt'))} files. Found {len(results)} lines matching 'ruleId: reentrancy'.")
