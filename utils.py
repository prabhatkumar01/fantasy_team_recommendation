import json
import os
from fuzzywuzzy import process

ground_stats = [
    {
        "groundName": "MA Chidambaram Stadium, Chepauk, Chennai",
        "stats": {
            "total_runs_scored": 22145,
            "wickets_taken": 795,
            "highest_score": "246/5",
            "best_bowling_figure": "5/5",
            "batting_average": 27.85,
            "batting_first_win_percentage": 58.9,
            "batting_second_win_percentage": 41.1,
            "strike_rate": 131.54,
            "pitch_type": "Bowling Friendly"
        }
    },
    {
        "groundName": "Sawai Mansingh Stadium, Jaipur",
        "stats": {
            "total_runs_scored": 15702,
            "wickets_taken": 512,
            "highest_score": "202/5",
            "best_bowling_figure": "6/14",
            "batting_average": 30.6,
            "batting_first_win_percentage": 34,
            "batting_second_win_percentage": 66,
            "strike_rate": 123.6,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "M Chinnaswamy Stadium, Bengaluru",
        "stats": {
            "total_runs_scored": 25745,
            "wickets_taken": 927,
            "highest_score": "263/5",
            "best_bowling_figure": "4/9",
            "batting_average": 27.8,
            "batting_first_win_percentage": 44.5,
            "batting_second_win_percentage": 55.5,
            "strike_rate": 141.8,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
        "stats": {
            "total_runs_scored": 1227,
            "wickets_taken": 69,
            "highest_score": "192/7",
            "best_bowling_figure": "4/29",
            "batting_average": 29.7,
            "batting_first_win_percentage": 33,
            "batting_second_win_percentage": 67,
            "strike_rate": 133,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Eden Gardens, Kolkata",
        "stats": {
            "total_runs_scored": 24407,
            "wickets_taken": 889,
            "highest_score": "263/5",
            "best_bowling_figure": "5/19",
            "batting_average": 27.45,
            "batting_first_win_percentage": 44.9,
            "batting_second_win_percentage": 55.1,
            "strike_rate": 138,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
        "stats": {
            "total_runs_scored": 3188,
            "wickets_taken": 137,
            "highest_score": "199/2",
            "best_bowling_figure": "5/14",
            "batting_average": 23.26,
            "batting_first_win_percentage": 54.55,
            "batting_second_win_percentage": 46.5,
            "strike_rate": 124.7,
            "pitch_type": "Bowling Friendly"
        }
    },
    {
        "groundName": "Narendra Modi Stadium, Ahmedabad",
        "stats": {
            "total_runs_scored": 8767,
            "wickets_taken": 325,
            "highest_score": "233/3",
            "best_bowling_figure": "5/10",
            "batting_average": 26.97,
            "batting_first_win_percentage": 45,
            "batting_second_win_percentage": 55,
            "strike_rate": 134.79,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Rajiv Gandhi International Stadium, Uppal, Hyderabad",
        "stats": {
            "total_runs_scored": 21256,
            "wickets_taken": 751,
            "highest_score": "277/3",
            "best_bowling_figure": "6/12",
            "batting_average": 28.3,
            "batting_first_win_percentage": 45.8,
            "batting_second_win_percentage": 54.2,
            "strike_rate": 133.5,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Wankhede Stadium, Mumbai",
        "stats": {
            "total_runs_scored": 31515,
            "wickets_taken": 1144,
            "highest_score": "235/1",
            "best_bowling_figure": "5/18",
            "batting_average": 27.5,
            "batting_first_win_percentage": 45.4,
            "batting_second_win_percentage": 54.6,
            "strike_rate": 136.1,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Arun Jaitley Stadium, Delhi",
        "stats": {
            "total_runs_scored": 23094,
            "wickets_taken": 842,
            "highest_score": "231/4",
            "best_bowling_figure": "5/13",
            "batting_average": 27.4,
            "batting_first_win_percentage": 46,
            "batting_second_win_percentage": 54,
            "strike_rate": 132.4,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
        "stats": {
            "total_runs_scored": 3910,
            "wickets_taken": 148,
            "highest_score": "206/4",
            "best_bowling_figure": "4/11",
            "batting_average": 26.41,
            "batting_first_win_percentage": 45.9,
            "batting_second_win_percentage": 54.1,
            "strike_rate": 136.7,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
        "stats": {
            "total_runs_scored": 3110,
            "wickets_taken": 125,
            "highest_score": "232/2",
            "best_bowling_figure": "4/14",
            "batting_average": 24.88,
            "batting_first_win_percentage": 63,
            "batting_second_win_percentage": 37,
            "strike_rate": 143,
            "pitch_type": "Batting Friendly"
        }
    },
    {
        "groundName": "Barsapara Cricket Stadium, Guwahati",
        "stats": {
            "total_runs_scored": 1124,
            "wickets_taken": 48,
            "highest_score": "225/3",
            "best_bowling_figure": "4/30",
            "batting_average": 23.98,
            "batting_first_win_percentage": 42,
            "batting_second_win_percentage": 58,
            "strike_rate": 133.5,
            "pitch_type": "Batting Friendly"
        }
    }
]

def find_ground_stats(ground_name):
    ground_names = [ground['groundName'] for ground in ground_stats]
    best_match, score = process.extractOne(ground_name, ground_names)
    if score < 70:  # You can adjust the threshold as needed
        return None
    for ground in ground_stats:
        if ground['groundName'] == best_match:
            return ground
    return None

def get_player_stats(player_id, opponent_team_name):
    file_path = f"./player-data/{player_id}_vsteam_stats.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as file:
            player_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    if 'overall_performance' not in player_data:
        return {}
    overall_performance = player_data['overall_performance']
    if opponent_team_name not in overall_performance:
        return {}
    team_stats = overall_performance[opponent_team_name]
    return team_stats

def get_player_stats_on_ground(playerName, playerId, ground):
    file_path = f"player_ground_stats/{playerId}_{ground.replace(' ', '_').replace(',', '')}.json"
    if not os.path.exists(file_path):
        print(f"No data found for {playerName} at {ground}")
        return {}
    try:
        with open(file_path, 'r') as file:
            player_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    return player_data
