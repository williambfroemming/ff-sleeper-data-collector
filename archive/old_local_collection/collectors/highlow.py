"""
High/Low Points Data Collector
Identifies weekly high and low scorers
"""

import pandas as pd
from typing import Dict
from utils.api import get_matchups
from utils.mappings import get_real_name


def collect_highlow_data(league_id: str, year: int, weeks: range,
                         roster_to_owner: Dict, owner_to_display: Dict,
                         name_map: Dict) -> pd.DataFrame:
    """
    Collect weekly high and low points data.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        weeks: Range of weeks to collect
        roster_to_owner: Mapping of roster_id -> owner_id
        owner_to_display: Mapping of owner_id -> display_name
        name_map: Mapping of display_name -> real_name
        
    Returns:
        DataFrame with weekly high/low scorers
    """
    print(f"  📈 Collecting high/low points data...")
    
    season_data = []
    
    for week in weeks:
        matchups = get_matchups(league_id, week)
        if not matchups:
            continue
            
        points_data = [
            {
                "display_name": get_real_name(
                    roster_to_owner[matchup["roster_id"]], 
                    owner_to_display, 
                    name_map
                ),
                "points": matchup["points"]
            }
            for matchup in matchups
        ]
        
        # Find min and max points entries
        min_points_entry = min(points_data, key=lambda x: x['points'])
        max_points_entry = max(points_data, key=lambda x: x['points'])
        
        season_data.append({
            "week": f"week{week}",
            "high points user": max_points_entry['display_name'],
            "high points": max_points_entry['points'],
            "low points user": min_points_entry['display_name'],
            "low points": min_points_entry['points']
        })
    
    return pd.DataFrame(season_data)
