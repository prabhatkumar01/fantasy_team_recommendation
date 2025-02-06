from google.cloud import storage
import csv
import io

def read_file_from_gcs():
    client = storage.Client()
    bucket = client.bucket('players_stats_credits')
    blob = bucket.blob('players_stats_credit.csv')
    file_content = blob.download_as_string()
    return file_content.decode('utf-8')

def filter_players_by_teams(csv_content, team1, team2):
    filtered_players = []
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    for row in csv_reader:
        if row['teamName'] == team1 or row['teamName'] == team2:
            filtered_players.append(row)
    
    return filtered_players

def getPlayingXI(team1, team2):
    csv_content = read_file_from_gcs()
    filtered_players = filter_players_by_teams(csv_content, team1, team2)
    
    return filtered_players