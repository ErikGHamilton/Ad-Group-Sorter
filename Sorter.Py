import csv
import os
#import pandas

csv_file_path = "data/keywordstats.csv"  #TODO - Make Dynamic

with open(csv_file_path, "r") as csv_file: # Code from class repository
    reader = csv.DictReader(csv_file) # assuming your CSV has headers
    for row in reader:
        print(row["keyword"], row["Currency"])
