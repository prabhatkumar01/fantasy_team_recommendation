# Fantasy Team Recommendation

This project provides a fantasy team recommendation system using Google Cloud services and a Flask web server. The system generates a fantasy team based on various parameters and validates the team according to predefined rules.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Python 3.9](https://www.python.org/downloads/)

## Installation

1. Install Google Cloud SDK:
    ```sh
    brew install --cask google-cloud-sdk
    ```

2. Initialize Google Cloud SDK:
    ```sh
    gcloud init
    ```

3. Authenticate with Google Cloud:
    ```sh
    gcloud auth application-default login
    ```

4. Install required Python packages:
    ```sh
    pip install --upgrade google-cloud-aiplatform
    pip install google-generativeai
    pip install google-genai
    pip install flask
    pip install flask-cors
    ```

## Running the Server

1. Start the Flask server:
    ```sh
    python server.py
    ```

## API Endpoints

### Generate Team

- **URL:** `/generate_team`
- **Method:** `POST`
- **Description:** Generates a fantasy team based on the provided parameters.
- **Request Body:**
    ```json
    {
        "team1": "Team1 Name",
        "team2": "Team2 Name",
        "groundName": "Ground Name",
        "risk_percentage": 50,
        "team_type": "Type",
        "team_count": 1,
        "point_system": "Point System",
        "players_info_1": [],
        "players_info_2": [],
        "rules": {},
        "scoreboards": {},
        "ground_stat": {}
    }
    ```
- **Response:**
    ```json
    {
        "data": {
            "fantasy_team": [
                {
                    "player_id": 123,
                    "name": "Player Name",
                    "role": "Batsman",
                    "team": "Team1",
                    "image_url": "Image URL"
                }
            ],
            "captain": {
                "player_id": 123,
                "name": "Player Name",
                "image_url": "Image URL"
            },
            "vice_captain": {
                "player_id": 123,
                "name": "Player Name",
                "image_url": "Image URL"
            }
        }
    }
    ```

### Get Players by Teams

- **URL:** `/get_players/team1/<team1_name>/team2/<team2_name>`
- **Method:** `GET`
- **Description:** Retrieves the players for the specified teams.
- **Response:**
    ```json
    {
        "team1": [],
        "team2": []
    }
    ```

