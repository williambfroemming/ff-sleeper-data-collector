"""
Data Collectors for Fantasy Football Statistics
Each collector module handles a specific type of data
"""

from .league_standings import collect_league_standings
from .matchups import collect_matchup_data
from .playoffs import collect_playoff_data
from .highlow import collect_highlow_data
from .players import collect_player_data

__all__ = [
    'collect_league_standings',
    'collect_matchup_data',
    'collect_playoff_data',
    'collect_highlow_data',
    'collect_player_data'
]
