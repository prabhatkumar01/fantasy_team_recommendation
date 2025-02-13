import csv
import json
import generatePrompt


def read_player_info_and_generate_prompt(csv_filepath):
    all_teams = set()
    player_info = {}

    with open(csv_filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            player_id = row['id']
            player_name = row['name']
            team_name = row['teamName']
            all_teams.add(team_name)
            player_info[player_id] = {
                'name': player_name,
                'teamName': team_name
            }
    prompts = {}
    for player_id, info in player_info.items():
        prompt = generatePrompt.generate_player_stats_prompt(player_id, info['name'], info['teamName'], all_teams)
        prompts[player_id] = prompt

    return prompts

# Example usage
csv_filepath = 'data/player.csv'
prompts = read_player_info_and_generate_prompt(csv_filepath)
for player_id, prompt in prompts.items():
    resp = generatePrompt.generate(prompt, True)
    filename = f"{player_id}_vsteam_stats.json"
    with open(filename, 'w') as json_file:
            if isinstance(resp, dict):
                json.dump(resp, json_file, indent=4)
            else:
                json.dump({"response": resp}, json_file, indent=4)
        
    print(f"Response for player {player_id} written to {filename}")