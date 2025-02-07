from google.cloud import storage, aiplatform
from google import genai
from google.genai import types

def generate_prompt(team1, team2, players_info_1, players_info_2, rules, scoreboards):

    prompt = f"Here are the details of the players in match for {team1}:\n\n"
    # prompt += "Player ID: '001', Name: 'anirudh', Roles: 'Batting', Team Name: 'RCB', Credit: '10', Matches: '300', Runs: '6000', Average: '70', Best Performance: '200', Wickets: '200', Economy: '15', Five Wicket Hauls: '10', Bowling Strike Rate: '20'\n"
    for player in players_info_1:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['roles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit ']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['avg']}, "
            f"Best Performance: {player['best_performance']}, Wickets: {player['wickets']}, "
            f"Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
    
    prompt += f"\nHere are the details of the players in match for {team2}:\n\n"
    for player in players_info_2:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['roles']}, "
            f"Team Name: {player['teamName']}, Credit: {player['credit ']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['avg']}, "
            f"Best Performance: {player['best_performance']}, Wickets: {player['wickets']}, "
            f"Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
    
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
    
    prompt += "\nBased on the above data, please create a fantasy team of 11 players using players from both teams in match that adheres to the given rules strictly."
    prompt += "You need to select a captain and a vice-captain from the team. The captain will get 2x points and the vice-captain will get 1.5x points.\n"
    prompt += "The team should be balanced and should not exceed the total credits. The team should have the right mix of roles as per the rules.\n"

    prompt += "Consider taking risks by 75% and selecting players who are not selected by others to get an edge over the competition.\n"
    prompt += "Provide the team in the following JSON format, including reasoning for selecting each player, credit calculations, and justifications:\n"
    prompt += "Also share me the response of not-selected players and the reason for not selecting them.\n"
    prompt += "Also share the count of batsmen, bowlers, allrounders, and wicketkeepers in the team.\n"
    prompt += "Also share all rules and if they are followed or not.\n"
    prompt += "Also share which player is considered with risk and why.\n"
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
    prompt += ' "not_selected_players": ['
    prompt += '    {"player_id": 123, "name": "Player1", "role": "Batsman", "credit": 9.5, "team": "(from players info)", "reason for not selecting": "High strike rate"},\n'
    prompt += ']\n'
    prompt += "}"

    return prompt

def generate(prompt_text):
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
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
