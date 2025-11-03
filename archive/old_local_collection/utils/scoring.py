"""
Fantasy scoring utilities
Calculates fantasy points based on player stats and league scoring settings
"""

from typing import Dict


def calculate_player_points(stats: Dict, scoring_settings: Dict) -> float:
    """
    Calculate fantasy points for a player based on their stats.
    
    Args:
        stats: Dictionary of player stats for the week
        scoring_settings: League scoring configuration
        
    Returns:
        Total fantasy points (rounded to 2 decimals)
    """
    if not stats:
        return 0.0
    
    points = 0.0
    
    for stat_key, stat_value in stats.items():
        if stat_key in scoring_settings and stat_value:
            points += scoring_settings[stat_key] * stat_value
    
    return round(points, 2)
