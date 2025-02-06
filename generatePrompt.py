from google.cloud import storage, aiplatform
from google import genai
from google.genai import types

def generate_prompt(players_info, rules, scoreboards):
    prompt = "Here are the details of the players in match:\n\n"
    for player in players_info:
        prompt += (
            f"Player ID: {player['id']}, Name: {player['name']}, Roles: {player['roles']}, "
            f"Team ID: {player['teamId']}, Team Name: {player['teamName']}, Credit: {player['credit ']}, "
            f"Matches: {player['match']}, Runs: {player['runs']}, Average: {player['avg']}, "
            f"Best Performance: {player['best_performance']}, Wickets: {player['wickets']}, "
            f"Economy: {player['economy']}, Five Wicket Hauls: {player['five_wicket']}, "
            f"Bowling Strike Rate: {player['bolwing_strike_rate']}\n"
        )
    
    prompt += "\nHere are the rules for creating a fantasy team:\n"
    prompt += f"Team Composition: {rules['team_composition']}\n"
    prompt += f"Credit System: {rules['credit_system']}\n"
    prompt += f"Player Selection Rules: {rules['player_selection_rules']}\n"
    
    prompt += "\nHere are the scoreboards:\n\n"
    for file_name, file_content in scoreboards.items():
        prompt += f"File: {file_name}\nContent:\n{file_content}\n\n"
    
    prompt += "\nBased on the above data, please create a fantasy team of 11 players using players in match that adheres to the given rules."
    prompt += "Provide the team in JSON format, including reasoning for selecting each player, credit calculations, and justifications."

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
