"""
League Standings Data Collector
Collects final season standings with wins, losses, and points
"""

import pandas as pd
from typing import List, Dict
from utils.mappings import calculate_points_with_decimal


def collect_league_standings(league_id: str, year: int, rosters: List[dict], 
                             users: List[dict], name_map: Dict) -> pd.DataFrame:
    """
    Collect league standings data.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        rosters: List of roster objects
        users: List of user objects
        name_map: Mapping of display names to real names
        
    Returns:
        DataFrame with league standings
    """
    print(f"  📊 Collecting league standings...")
    
    # Map user IDs to display names
    user_display_names = {entry['user_id']: entry['display_name'] for entry in users}
    
    member_data = [
        {
            "Member": name_map.get(
                user_display_names.get(roster["owner_id"]), 
                user_display_names.get(roster["owner_id"])
            ),
            "Year": year,
            "Wins": roster.get("settings", {}).get("wins", 0),
            "Losses": roster.get("settings", {}).get("losses", 0),
            "Points For": calculate_points_with_decimal(roster.get("settings", {}), "fpts"),
            "Points Against": calculate_points_with_decimal(roster.get("settings", {}), "fpts_against"),
        }
        for roster in rosters
    ]
    
    # Create DataFrame and sort by standings
    df = pd.DataFrame(member_data)
    df = df.sort_values(by=["Wins", "Points For"], ascending=[False, False])
    df = df.reset_index(drop=True)
    df["Place"] = range(1, len(df) + 1)
    
    # Reorder columns
    df = df[["Member", "Year", "Place", "Wins", "Losses", "Points For", "Points Against"]]
    
    return df
