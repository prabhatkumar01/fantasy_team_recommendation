import json
import csv
import requests

def fetch_all_matches_data():
    url = "https://pp-hs-consumer-api.espncricinfo.com/v1/pages/series/schedule?seriesId=1410320"

    payload = {}
    headers = {

    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()

    matches = response_json.get('content', {}).get('matches', [])
    match_ids = [match.get('objectId') for match in matches]
    
    return match_ids

def fetch_and_store_batsmen_data(match_id):
    url = f"https://pp-hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?seriesId=1410320&matchId={match_id}"

    payload = {}
    headers = {

    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response_json = response.json()

    innings = response_json.get('content', {}).get('innings', [])

    with open(f'inning_bowler_{match_id}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Name', "Bowled Type", 'Overs', 'Balls', 'Maidens', 'Runs Conceded', 'Wickets', 'Economy', 'Runs Per Ball', 'Dots', 'Fours', 'Sixes', 'Wides', 'No Balls'])

        for inning in innings:
            inning_bowlers = inning.get('inningBowlers', [])
            for bowler in inning_bowlers:
                player = bowler.get('player', {})
                writer.writerow([
                    player.get('name'),
                    bowler.get('bowledType'),
                    bowler.get('overs'),
                    bowler.get('balls'),
                    bowler.get('maidens'),
                    bowler.get('conceded'),
                    bowler.get('wickets'),
                    bowler.get('economy'),
                    bowler.get('runsPerBall'),
                    bowler.get('dots'),
                    bowler.get('fours'),
                    bowler.get('sixes'),
                    bowler.get('wides'),
                    bowler.get('noBalls'),
                ])

# Call the function to fetch all matches data and store in an array
match_ids = fetch_all_matches_data()

# Iterate through each match ID and call fetch_and_store_batsmen_data
for match_id in match_ids:
    fetch_and_store_batsmen_data(match_id)