"""
Historical Player Totals Collector
Gets season totals for ALL players across multiple years
Used for draft value analysis via VLOOKUP
"""

import pandas as pd
from typing import List
from utils.api import get_weekly_stats, get_all_players
from utils.scoring import calculate_player_points


def collect_historical_player_totals(years: List[int], scoring_settings: dict) -> pd.DataFrame:
    """
    Collect season totals for all players across multiple years.
    This creates a lookup table for draft analysis.
    Uses weeks 1-17 (full fantasy season including playoffs).
    
    Args:
        years: List of years to collect (e.g., [2021, 2022, 2023, 2024])
        scoring_settings: League scoring configuration
        
    Returns:
        DataFrame with player season totals for VLOOKUP
    """
    print(f"\n  Collecting historical player totals for {len(years)} years (weeks 1-17)...")
    
    # Get players map once
    players_map = get_all_players()
    
    all_player_totals = []
    
    # Use full fantasy season (weeks 1-17)
    weeks = range(1, 18)
    
    for year in years:
        print(f"    Processing {year}...")
        year_totals = {}
        
        for week in weeks:
            weekly_stats = get_weekly_stats(year, week)
            
            for player_id, stats in weekly_stats.items():
                if player_id not in year_totals:
                    year_totals[player_id] = {
                        'stats': {},
                        'weeks_played': 0
                    }
                
                # Accumulate stats
                for stat_key, stat_value in stats.items():
                    if stat_key not in year_totals[player_id]['stats']:
                        year_totals[player_id]['stats'][stat_key] = 0
                    if stat_value:
                        year_totals[player_id]['stats'][stat_key] += stat_value
                
                year_totals[player_id]['weeks_played'] += 1
        
        # Calculate fantasy points for each player
        for player_id, player_data in year_totals.items():
            player_info = players_map.get(player_id, {})
            total_points = calculate_player_points(player_data['stats'], scoring_settings)
            
            player_name = f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip() or player_id
            
            all_player_totals.append({
                'year': year,
                'player_id': player_id,
                'player_name': player_name,
                'position': player_info.get('position', 'Unknown'),
                'nfl_team': player_info.get('team', 'FA'),
                'weeks_played': player_data['weeks_played'],
                'total_fantasy_points': round(total_points, 2),
                'avg_points_per_game': round(total_points / player_data['weeks_played'], 2) if player_data['weeks_played'] > 0 else 0
            })
    
    df = pd.DataFrame(all_player_totals)
    
    # Sort by year and total points
    df = df.sort_values(['year', 'total_fantasy_points'], ascending=[True, False])
    
    print(f"    ✓ Collected totals for {len(df)} player-seasons")
    
    return df