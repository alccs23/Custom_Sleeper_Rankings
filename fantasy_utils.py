import csv
import requests
import re

def normalize_name(name):
    '''
    Normalizes a full name by removing suffixes and special characters,
    and collapsing whitespace to match names between sources.
    '''
    name = re.sub(r'\b(Jr\.?|Sr\.?|II|III|IV|V)\b', '', name)
    name = re.sub(r'[^a-zA-Z\s\-]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip().lower()

def get_draft_pick_names(draft_id):
    '''
    Fetches draft picks from Sleeper's API and returns a set of normalized full names
    for the given draft ID.
    '''
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    response = requests.get(url)
    data = response.json()
    return set(normalize_name(f"{p['metadata']['first_name']} {p['metadata']['last_name']}") for p in data if 'metadata' in p)

def get_filtered_fantasy_rankings(csv_file_path, drafted_names):
    '''
    Reads a fantasy football CSV ranking file and returns an ordered list of players
    excluding any whose normalized names appear in the drafted_names set.
    '''
    filtered_list = []
    with open(csv_file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["PLAYER NAME"].strip()
            team = row["TEAM"].strip()
            pos = row["POS"].strip()
            rank = row["RK"].strip()
            norm_name = normalize_name(name)
            if norm_name not in drafted_names:
                filtered_list.append(f"{rank}. {name} ({team}, {pos})")
    return filtered_list

