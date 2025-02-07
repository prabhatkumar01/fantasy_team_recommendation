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
    team1_players = []
    team2_players = []
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    for row in csv_reader:
        if row['teamName'] == team1:
            team1_players.append(row)
        elif row['teamName'] == team2:
            team2_players.append(row)
    
    return team1_players, team2_players

def getPlayingXI(team1, team2):
    csv_content = read_file_from_gcs()
    team1_players, team2_players = filter_players_by_teams(csv_content, team1, team2)
    return team1_players, team2_players
