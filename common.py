import csv
import os

# Parse imdb data and return an array of each line

logo = """
  __  __                   _           _____                                _     
 |  \/  |                 (_)         / ____|                              | |    
 | \  / |   ___   __   __  _    ___  | (___     ___    __ _   _ __    ___  | |__  
 | |\/| |  / _ \  \ \ / / | |  / _ \  \___ \   / _ \  / _` | | '__|  / __| | '_ \ 
 | |  | | | (_) |  \ V /  | | |  __/  ____) | |  __/ | (_| | | |    | (__  | | | |
 |_|  |_|  \___/    \_/   |_|  \___| |_____/   \___|  \__,_| |_|     \___| |_| |_|
"""

def print_logo():
    os.system('clear')
    green = "\033[32m"
    reset = "\033[0m"

    print(f"{green}{logo}{reset}\n")

def parse_csv(csv_file_path):
    csv_file = open(csv_file_path, "r")
    csv_reader = csv.DictReader(csv_file)

    lines = []

    for row in csv_reader:
        line = f'Title: {row["Series_Title"]}, Released on: {row["Released_Year"]}, Length: {row["Runtime"]}, ' \
            f'Genre: {row["Genre"]}, IMDB Rating: {row["IMDB_Rating"]}, Number of Votes: {row["No_of_Votes"]}, Overview/Summary: {row["Overview"]}, Meta Score: {row["Meta_score"]}, '  \
            f'Director: {row["Director"]}, Actor1: {row["Star1"]}, Actor2: {row["Star2"]}, Actor3: {row["Star3"]}, Actor4: {row["Star4"]}'

        lines.append(line)

    csv_file.close()

    return lines