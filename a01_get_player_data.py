import json
import os

import httpx
from tqdm import tqdm


def get_player_data():
    r = httpx.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    bs = r.json()
    players = bs.get("elements")
    print("Fetching players")
    for p in tqdm(players):
        player_id = str(p["id"])
        r = httpx.get(
            f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        )
        player_info = r.json()
        p["summary"] = player_info
    return players


def save_data(data):
    # Ensure that the data directory exists
    if not os.path.exists("data"):
        os.mkdir("data")

    file_path = "data/player_data.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)
    print("Player data written to", file_path)


if __name__ == "__main__":
    save_data(get_player_data())
