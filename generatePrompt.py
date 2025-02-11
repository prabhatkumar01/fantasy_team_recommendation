from google.cloud import storage, aiplatform
from google import genai
import json
import utils
from google.genai import types

def generate_player_performance_prompt(player_name, ground_name):
    prompt = f"""
    Fetch the performance details of the player {player_name} at the ground {ground_name} for the following IPL seasons: 2019, 2020, 2021, 2022, 2023, and 2024. The details should include:
    - Scores
    - Wickets taken
    - Highest score
    - Best bowling figure
    - Batting average
    - Teams winning batting first
    - Teams winning batting second
    - Strike rate

    Please provide the data in JSON format.
    """
    return prompt

def generate_autofill_prompt(team1, team2, players_info_1, players_info_2, rules, scoreboards, selected_players):
    prompt = f"Here are the details of the players in match for {team1}:\n\n"
    # prompt += "Player ID: '001', Name: 'anirudh', Roles: 'Batting', Team Name: 'RCB', Credit: '10', Matches: '300', Runs: '6000', Average: '70', Best Performance: '200', Wickets: '200', Economy: '15', Five Wicket Hauls: '10', Bowling Strike Rate: '20'\n"
    for player in players_info_1:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['playingRoles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['batting_avg']}, "
            f"Wickets: {player['wickets']}, Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
    
    prompt += f"\nHere are the details of the players in match for {team2}:\n\n"
    for player in players_info_2:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['playingRoles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['batting_avg']}, "
            f"Wickets: {player['wickets']}, Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )

    prompt += "\nUser has already selected the following players for the fantasy team:\n"
    for player in selected_players:
        prompt += (
            f"Name: {player}"
        )

    prompt += f"\nFill the remaining {11 - len(selected_players)} players to complete the team while following these rules strictly:\n"
    prompt += f"Team Composition: {rules['team_composition']}\n"
    prompt += f"  Total Players: {rules['team_composition']['total_players']}\n"
    for role, limits in rules['team_composition']['roles'].items():
        prompt += f"  {role.capitalize()}: Min {limits['min']}, Max {limits['max']}\n"
    prompt += f"Credit System: Total Credits {rules['credit_system']['total_credits']}\n"
    prompt += "Player Selection Rules:\n"
    prompt += f"  Max Players Per Team: {rules['player_selection_rules']['max_players_per_team']}\n"
    prompt += f"  Captain Multiplier: {rules['player_selection_rules']['captain_multiplier']}\n"
    prompt += f"  Vice Captain Multiplier: {rules['player_selection_rules']['vice_captain_multiplier']}\n"

    prompt += "\nEnsure the final team follows all rules and remains within the credit limit.\n"
    prompt += "Select a captain and vice-captain, ensuring they are impactful players.\n"

    prompt += "Provide the response in the following JSON format:\n"
    prompt += "{\n"
    prompt += '  "fantasy_team": [\n'
    prompt += '    {"player_id": 123, "name": "Player1", "role": "Batsman", "credit": 9.5, "team": "(from players info)", "reason": "High strike rate"},\n'
    prompt += '    {"player_id": 456, "name": "Player2", "role": "Allrounder", "credit": 10.0, "team": "(from players info)", "reason": "Consistent wicket-taker"},\n'
    prompt += "    ...\n"
    prompt += "  ],\n"
    prompt += '  "captain": {"player_id": 789, "name": "PlayerX", "reason": "High impact performance in last 3 matches"},\n'
    prompt += '  "vice_captain": {"player_id": 101, "name": "PlayerY", "reason": "Best batting average among all players"},\n'
    prompt += '  "total_credit_used": 99.5,\n'
    prompt += '  "team_balance": {"CSK": 5, "KKR": 6},\n'
    prompt += '  "validation": {\n'
    prompt += '     "roles_valid": true,\n'
    prompt += '     "team_balance_valid": true,\n'
    prompt += '     "credit_usage_valid": true\n'
    prompt += "  }\n"
    prompt += '}\n'

    return prompt


def generate_team_prompt(team1, team2, players_info_1, players_info_2, rules, scoreboards, ground,  risk_percentage, team_type, team_count, point_system):
    prompt = f"Here are the details of the players in match for {team1}:\n\n"
    for player in players_info_1:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['playingRoles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['batting_avg']}, "
            f"Wickets: {player['wickets']}, Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
        # Add player stats for the opponent team
        player_stats = utils.get_player_stats(player['id'], team2)
        if player_stats:
            prompt += f"Player Stats against Oponent {team2}: {json.dumps(player_stats, indent=4)}\n"
    
    prompt += f"\nHere are the details of the players in match for {team2}:\n\n"
    for player in players_info_2:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['playingRoles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['batting_avg']}, "
            f"Wickets: {player['wickets']}, Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
        # Add player stats for the opponent team
        player_stats = utils.get_player_stats(player['id'], team1)
        if player_stats:
            prompt += f"Player Stats against Oponent {team1}: {json.dumps(player_stats, indent=4)}\n"

    prompt += "Use above info as players info to find players info regarding teamName and their career stats.\n"

    prompt += "\nHere are the rules for creating a fantasy team:\n"
    prompt += f"Team Composition: {rules['team_composition']}\n"
    prompt += f"  Total Players: {rules['team_composition']['total_players']}\n"
    for role, limits in rules['team_composition']['roles'].items():
        prompt += f"  {role.capitalize()}: Min {limits['min']}, Max {limits['max']}\n"
    prompt += f"Credit System: Total Credits {rules['credit_system']['total_credits']}\n"
    prompt += "Player Selection Rules:\n"
    prompt += f"  Max Players Per Team: {rules['player_selection_rules']['max_players_per_team']}\n"
    prompt += f"  Captain Multiplier: {rules['player_selection_rules']['captain_multiplier']}\n"
    prompt += f"  Vice Captain Multiplier: {rules['player_selection_rules']['vice_captain_multiplier']}\n"
    prompt += "These rules should be strictly followed while creating the fantasy team.\n"
    
    prompt += "\nHere are the scoreboards:\n\n"
    for file_name, file_content in scoreboards.items():
        prompt += f"File: {file_name}\nContent:\n{file_content}\n\n"
        
    prompt += "\nHere are the ground stats:\n\n"
    prompt += f"Ground Name: {ground['groundName']}\n"
    for stat, value in ground['stats'].items():
        prompt += f"{stat.replace('_', ' ').capitalize()}: {value}\n"
    
    prompt += f"\nBased on the above data, please create {team_count} different fantasy teams of 11 players each, following the given rules strictly. "
    prompt += f"Each team should be formed using the {team_type} strategy, Ground Stats,Ground pitch type and should have slightly different player combinations. "
    prompt += f"Give more weight to player stats against Oponent, Career stats and player ground stats while selecting {risk_percentage}% of players in the team.\n"
    prompt += "Your goal is to select a team which will collect maximum points in the match.\n"
    prompt += "Here is the points system:\n"
    prompt += json.dumps(point_system, indent=4)
    # prompt += "Consider selecting players who are not selected by others to get an edge over the competition.\n"
    prompt += "Provide the team in the following JSON format, including reasoning for selecting each player, credit calculations, and justifications in JSON only:\n"
    # prompt += "Also share me the response of not-selected players and the reason for not selecting them.\n"
    #prompt += "Also share the count of batsmen, bowlers, allrounders, and wicketkeepers in the team.\n"
    #prompt += "Also share all rules and if they are followed or not.\n"
    # prompt += "Also share which player is considered with risk and why.\n"
    prompt += "The JSON format should be as follows:\n"
    prompt += "{\n"
    prompt += '  "fantasy_team": [\n'
    prompt += '    {"player_id": 123, "name": "Player1", "role": "Batsman", "credit": 9.5, "team": "(from players info)", "reason": "High strike rate"},\n'
    prompt += '    {"player_id": 456, "name": "Player2", "role": "Allrounder", "credit": 10.0, "team": "(from players info)", "reason": "Consistent wicket-taker"},\n'
    prompt += "    ...\n"
    prompt += "  ],\n"
    prompt += '  "captain": {"player_id": 789, "name": "PlayerX", "reason": "High impact performance in last 3 matches"},\n'
    prompt += '  "vice_captain": {"player_id": 101, "name": "PlayerY", "reason": "Best batting average among all players"},\n'
    prompt += '  "total_credit_used": 99.5,\n'
    prompt += '  "team_balance": {"CSK": 5, "KKR": 6},\n'
    prompt += '  "validation": {\n'
    prompt += '     "roles_valid": true,\n'
    prompt += '     "team_balance_valid": true,\n'
    prompt += '     "credit_usage_valid": true\n'
    prompt += "  }\n"
    # prompt += ' "not_selected_players": ['
    # prompt += '    {"player_id": 123, "name": "Player1", "role": "Batsman", "credit": 9.5, "team": "(from players info)", "reason for not selecting": "High strike rate"},\n'
    # prompt += ']\n'
    prompt += "}"

    return prompt

def generate_player_stats_prompt(player_id, player_name, player_team, all_teams):
    other_teams = [team for team in all_teams if team != player_team]
    prompt = f"""
    Fetch the overall performance stats details of the player {player_name} (ID: {player_id}) against the following teams: {', '.join(other_teams)}. The details should include:
    - Total Runs Scored
    - Totoal Wickets taken
    - Highest score
    - Best bowling figure
    - Batting average
    - Teams winning batting first
    - Teams winning batting second
    - Batting Strike rate
    - Bowling Strike rate

    Please provide the data in JSON format.
    """
    return prompt

def generate(prompt_text, isJsonResponse=False):
    client = genai.Client(
        vertexai=True,
        project="jistar-hack25bom-208",
        location="us-central1",
    )

    model = "gemini-2.0-flash-001"
    
    # Add the prompt to the request
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt_text)]  # Pass the prompt here
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=6400,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
    )

    # Generate response
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text

    if isJsonResponse:
        # Remove leading and trailing triple backticks and the 'json' keyword
        response_text = response_text.strip().strip('```').strip()
        if response_text.startswith('json'):
            response_text = response_text[len('json'):].strip()

        # Parse the response to ensure it is in JSON format
        try:
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            return {"error": "The response is not in valid JSON format", "response_text": response_text}
    else:
        return response_text
