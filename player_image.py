import requests
import csv
import json

def get_player_image(player_id):
    url = f"https://pp-hs-consumer-api.espncricinfo.com/v1/pages/player/images?playerId={player_id}"

    payload = {}
    headers = {
        'accept': 'application/json',
        'x-hsci-auth-key': ''
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            player_data = data.get('player')
            if player_data is None:
                print(f"No player data found for player ID: {player_id}")
                return "Player data not found"
            
            image_data = player_data.get('image')
            if image_data is None:
                print(f"No image data found for player ID: {player_id}")
                return "Image data not found"
            
            image_url = image_data.get('url')
            if image_url is None:
                print(f"No image URL found for player ID: {player_id}")
                return "Image URL not found"
        
            return "https://img1.hscicdn.com/image/upload/f_auto,t_h_100_2x" + image_url
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return "Error decoding JSON"
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"


def read_player_csv_and_fetch_images(file_path):
    players = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            player_id = row['id']
            player_name = row['name']
            image_url = get_player_image(player_id)
            row['image_url'] = image_url
            players.append(row)
    
    # Save the updated data back to the CSV file
    fieldnames = players[0].keys()
    with open('data/player.csv', mode='w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(players)

# Example usage
file_path = 'player_2.csv'
read_player_csv_and_fetch_images(file_path)