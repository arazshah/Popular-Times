from scraper import Scrap
import argparse


def process_links(input_file):

    # Read the CSV file into a pandas DataFrame
    txt_file = open(input_file, 'r')
    lines = [line.strip() for line in txt_file]  # remove trailing
    # CR/LF characters, if present.
    return lines


# Define command-line arguments using argparse
parser = argparse.ArgumentParser(description='Process data from a CSV file.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file')

# Parse the command-line arguments
args = parser.parse_args()
links = process_links(args.input_file)
scrp = Scrap("")
for link in links:
    scrp.url = link
    scrp.run()
