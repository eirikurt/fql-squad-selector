import json
from typing import Tuple

import numpy as np
from tabulate import tabulate

from _types import Player

#############################################
# Things to tweak before running the script #
#############################################

# The number of positions to fill. Lower these if you've already picked players for your bench
# and/or that one player you plan to captain every week.
# The order is [goalkeepers, defenders, midfielders, forwards]
empty_positions = [1, 3, 4, 3]

# Players that you want to exclude from the selection. For example, if you've already picked Haaland
# and just want to fill up the rest of the team, then put his id in this list.
# To find a player's id, consult data/player_data.json
# Examples based on ids from the 24/25 season
#  - [351] to exclude Haaland
#  - [328] to exclude Salah
#  - [328, 351] to exclude Salah and Haaland
blacklisted_player_ids: list[int] = []

# Your remaining budget in £ millions
budget = 82.9

# How to score players. A simple predictor of future performance is how many points they accrue per game.
# A more elaborate function, that takes future fixtures into account, would likely yield better results.
utility_function = lambda player: float(player["points_per_game"])

# We are only allowed 3 players from each team. If the script ends up picking more than that from one team,
# then change this to the number of that team. For the 24/25 season, the team numbers are as follows:
# 1.  Arsenal
# 2.  Aston Villa
# 3.  Bournemouth
# 4.  Brentford
# 5.  Brighton
# 6.  Chelsea
# 7.  Crystal Palace
# 8.  Everton
# 9.  Fulham
# 10. Ipswich
# 11. Leicester
# 12. Liverpool
# 13. Man City
# 14. Man Utd
# 15. Newcastle
# 16. Nottingham Forest
# 17. Southampton
# 18. Tottenham
# 19. West Ham
# 20. Wolves
dominant_team_number = 1

#############################################
# The code that does the actual work        #
#############################################


def main():
    players = load_players()

    # Score the players
    for p in players:
        p["utility"] = utility_function(p)

    # Remove undesirable players from the selection pool
    filtered_players = filter_players(players)

    print(f"Picking squad from a pool of {len(filtered_players)} players. This will take some time...")
    _, selection = select_team(0, int(budget * 10), filtered_players, empty_positions, 3)

    # Sort by position, then reveal...
    team = sorted([filtered_players[i] for i in selection], key=lambda p: p["element_type"])
    print_players(team)


def load_players() -> list[Player]:
    with open("data/player_data.json", mode="r") as file:
        return json.load(file)


def filter_players(players: list[Player]) -> list[Player]:
    return [
        p
        for p in players
        if p["utility"] > 0
        and p["id"] not in blacklisted_player_ids
        and p["starts"] > 2  # Exclude few-game wonders
        and (
            p["chance_of_playing_next_round"] is None  # Sometimes not available
            or p["chance_of_playing_next_round"] == 100
        )
    ]


def print_players(players: list[Player]):
    positions = ["gk", "def", "mid", "fwd"]
    formatted_players = [
        {
            "id": p["id"],
            "name": p["first_name"] + " " + p["second_name"],
            "cost": p["now_cost"] / 10.0,
            "points": p["total_points"],
            "form": p["form"],
            "utility": p["utility"],
            "team_nr": p["team"],
            "position": positions[p["element_type"] - 1],
        }
        for p in players
    ]
    print(tabulate(formatted_players, headers="keys"))


def select_team(
    start_index: int,
    budget_left: int,
    player_list: list[Player],
    empty_places: list[int],
    dominant_players_left: int,
    cache: np.ndarray | None = None,
) -> Tuple[float, list[int]]:
    if budget_left <= 0 or start_index >= len(player_list) or all(p == 0 for p in empty_places):
        return 0, []

    if cache is None:
        cache = np.empty(
            (
                len(player_list),
                budget_left + 1,
                empty_places[0] + 1,
                empty_places[1] + 1,
                empty_places[2] + 1,
                empty_places[3] + 1,
                4,
            ),
            dtype="O",
        )

    cache_index = (
        start_index,
        budget_left,
        empty_places[0],
        empty_places[1],
        empty_places[2],
        empty_places[3],
        dominant_players_left,
    )
    cached_result = cache[cache_index]
    if cached_result != None:
        return cached_result

    current_player = player_list[start_index]
    cost = current_player["now_cost"]
    position = current_player["element_type"] - 1
    from_dominant_team = 0
    if current_player["team"] == dominant_team_number:
        from_dominant_team = 1

    # Option A includes the current player, assuming that we can fit him in
    utility_a = 0.0
    selection_a: list[int] = []
    if cost <= budget_left and empty_places[position] > 0 and (dominant_players_left - from_dominant_team >= 0):
        # Fill remaining spots, assuming that we keep the current player
        updated_empty_places = empty_places.copy()
        updated_empty_places[position] = updated_empty_places[position] - 1
        utility, selection = select_team(
            start_index + 1,
            budget_left - cost,
            player_list,
            updated_empty_places,
            dominant_players_left - from_dominant_team,
            cache,
        )

        # Add the current player to the results
        utility_a = utility + current_player["utility"]
        selection_a = selection + [start_index]

    # Option B omits the current player
    utility_b, selection_b = select_team(
        start_index + 1,
        budget_left,
        player_list,
        empty_places,
        dominant_players_left,
        cache,
    )

    # Pick the better option
    result = (utility_a, selection_a) if utility_a > utility_b else (utility_b, selection_b)

    cache[cache_index] = result
    return result


if __name__ == "__main__":
    main()
