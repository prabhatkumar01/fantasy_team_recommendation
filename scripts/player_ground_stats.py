import csv
import json
import os
from google.cloud import storage, aiplatform
from google import genai
from google.genai import types
import queue
import threading

# Thread pool size
NUM_WORKERS = 100
task_queue = queue.Queue()

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]

def get_player_stats(player_name, ground_name):
    # This function should return the stats of the player in the given ground.
    # For simplicity, we will return dummy data here.
    # In a real scenario, you would fetch this data from a database or another source.
    return {
        "ground_name": ground_name,
        "matches": 3,
        "runs": 165,
        "wickets": 0,
        "batting_average": 82.50,
        "batting_strike_rate": 148.64,
        "bowling_strike_rate": None,
        "high_score": 98,
        "best_bowling": None,
        "50s": 1,
        "100s": 0,
        "5_wickets": 0
    }

def generate_player_ground_stats():
    grounds = read_csv('ground.csv')
    players = read_csv('player.csv')
    
    player_ground_stats = []
    
    for player in players:
        player_name = player['name']
        player_id = player['id']
        ground_stats = []
        
        for ground in grounds:
            ground_name = ground['Name']
            stats = get_player_stats(player_name, ground_name)
            ground_stats.append(stats)
        
        player_ground_stats.append({
            "player_name": player_name,
            "id": player_id,
            "ground_stats": ground_stats
        })
    
    return player_ground_stats

def generate_player_performance_prompt(player_name, ground_name):
    prompt = f"""
    Fetch the performance details of the player {player_name} at the ground {ground_name} for the following IPL seasons: 2021, 2022, 2023, and 2024. The details should include:
    - Scores
    - Wickets taken
    - Highest score
    - Best bowling figure
    - Batting average
    - Strike rate

    Please provide the data in JSON format, with season-wise stats. Do not include any team-related stats or other information like disclaimers or reasons.
    Here is an example of the expected JSON structure: Use it as sample for json structure
    Provide correct and detailed data for complete ipl season.
    {{
        "player": "player",
        "ground": "ground",
        "stats": {{
            "2019": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }},
            "2020": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }},
            "2021": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }},
            "2022": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }},
            "2023": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }},
            "2024": {{
                "scores": [],
                "wickets": 0,
                "highest_score": 0,
                "best_bowling_figure": "0/0",
                "batting_average": 0,
                "strike_rate": 0
            }}
        }}
    }}
    
    Don't provide any additional information or context. Just the raw data as specified above.
    """
    return prompt

def remove_first_line(text):
    lines = text.split("\n")  # Split text into lines
    return "\n".join(lines[1:-1]) if len(lines) > 2 else ""

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
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text

    return response_text

def save_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def worker():
    """Worker thread function to process generate tasks."""
    while True:
        try:
            player, ground_stat = task_queue.get(timeout=10)  # Timeout to prevent infinite blocking
        except queue.Empty:
            return  # Exit if no more tasks are available
        
        player_name = player['player_name']
        player_id = player['id']
        ground_name = ground_stat['ground_name']

        file_name = f"player_ground_stats/{player_id}_{ground_name.replace(' ', '_').replace(',', '')}.json"

        # Check if the file already exists
        if os.path.exists(file_name):
            print(f"File {file_name} already exists. Skipping...")
            task_queue.task_done()
            continue
        
        prompt = generate_player_performance_prompt(player_name, ground_name)
        json_response = generate(prompt)
        res = remove_first_line(json_response)
        print(res)
        try:
            json_data = json.loads(res)  # Convert text to JSON
            save_json_to_file(json_data, file_name)
        except json.JSONDecodeError as e:
            error_log = {
                "error": str(e),
                "response": res,
                "player_name": player_name,
                "ground_name": ground_name
            }
            log_error_to_file(error_log, "error_log.json")
            print("Invalid JSON:", e)

        task_queue.task_done()


# Generate the player ground stats
player_ground_stats = generate_player_ground_stats()

def log_error_to_file(error_log, file_path):
    with open(file_path, 'a') as file:
        file.write(json.dumps(error_log, indent=4) + "\n")


for player in player_ground_stats:
    for ground_stat in player['ground_stats']:
        task_queue.put((player, ground_stat))

threads = []
for _ in range(NUM_WORKERS):
    t = threading.Thread(target=worker, daemon=True)  # Daemon threads will exit when the main program exits
    t.start()
    threads.append(t)

    # Wait until all tasks are completed
task_queue.join()

print(json.dumps(player_ground_stats, indent=4))