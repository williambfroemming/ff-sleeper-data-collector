"""
Regular Season Data Collector
Collects season standings with wins, losses, and points
Outputs to: auto_stg_regular_season
"""

import pandas as pd
from typing import List, Dict
from utils.mappings import calculate_points_with_decimal


def collect_regular_season_data(league_id: str, year: int, rosters: List[dict], 
                             users: List[dict], name_map: Dict) -> pd.DataFrame:
    """
    Collect regular season standings data.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        rosters: List of roster objects
        users: List of user objects
        name_map: Mapping of display names to real names
        
    Returns:
        DataFrame with regular season standings
    """
    print(f"  Collecting regular season standings...")
    
    # Map user IDs to display names
    user_display_names = {entry['user_id']: entry['display_name'] for entry in users}
    
    member_data = [
        {
            "member_id": int(name_map.get(
                user_display_names.get(roster["owner_id"]), 
                user_display_names.get(roster["owner_id"])
            )),
            "wins": roster.get("settings", {}).get("wins", 0),
            "losses": roster.get("settings", {}).get("losses", 0),
            "points_scored": calculate_points_with_decimal(roster.get("settings", {}), "fpts"),
            "points_against": calculate_points_with_decimal(roster.get("settings", {}), "fpts_against"),
        }
        for roster in rosters
    ]

    # Create DataFrame and sort by standings
    df = pd.DataFrame(member_data)
    df = df.sort_values(by=["wins", "points_scored"], ascending=[False, False])
    df = df.reset_index(drop=True)
    df["place"] = range(1, len(df) + 1)

    # Reorder columns
    df = df[["member_id", "place", "wins", "losses", "points_scored", "points_against"]]
    
    return df
