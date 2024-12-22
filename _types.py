from typing import TypedDict


class Player(TypedDict):
    id: int
    first_name: str
    second_name: str
    form: float
    team: int
    now_cost: int
    total_points: int
    element_type: int
    points_per_game: float
    chance_of_playing_next_round: int | None
    starts: int
    utility: float
    # Loads more could be added, see /data/player_data.json for available attributes
