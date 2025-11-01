"""
Player Details Data Collector
Collects individual player statistics and fantasy points by team
Outputs to: stg_player_details_by_team
"""

import pandas as pd
from typing import Dict
from utils.api import get_matchups, get_weekly_stats, get_all_players
from utils.mappings import get_real_name
from utils.scoring import calculate_player_points


def collect_player_details_by_team_data(league_id: str, year: int, weeks: range,
                        roster_to_owner: Dict, owner_to_display: Dict,
                        name_map: Dict, scoring_settings: Dict) -> pd.DataFrame:
    """
    Collect player-level data for all weeks by team.
    This includes individual player fantasy points.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        weeks: Range of weeks to collect
        roster_to_owner: Mapping of roster_id -> owner_id
        owner_to_display: Mapping of owner_id -> display_name
        name_map: Mapping of display_name -> real_name
        scoring_settings: League scoring configuration
        
    Returns:
        DataFrame with player-level data by team
    """
    print(f"  Collecting player details by team (this may take a while)...")
    
    # Get players map once
    players_map = get_all_players()
    
    all_player_data = []
    
    for week in weeks:
        print(f"    Processing Week {week}...")
        
        matchups = get_matchups(league_id, week)
        if not matchups:
            continue
        
        # Get weekly stats for all players
        weekly_stats = get_weekly_stats(year, week)
        
        for matchup in matchups:
            roster_id = matchup['roster_id']
            owner_id = roster_to_owner.get(roster_id)
            team_name = get_real_name(owner_id, owner_to_display, name_map)
            
            starters = matchup.get('starters', [])
            all_players = matchup.get('players', [])
            
            for player_id in all_players:
                if not player_id:
                    continue
                
                is_starter = player_id in starters
                player_info = players_map.get(player_id, {})
                player_stats = weekly_stats.get(player_id, {})
                
                # Calculate fantasy points
                fantasy_points = calculate_player_points(player_stats, scoring_settings)
                
                # Extract key stats (will be NaN if not applicable for position)
                stats_dict = {
                    # Passing
                    'pass_yd': player_stats.get('pass_yd', None),
                    'pass_td': player_stats.get('pass_td', None),
                    'pass_int': player_stats.get('pass_int', None),
                    'pass_att': player_stats.get('pass_att', None),
                    'pass_cmp': player_stats.get('pass_cmp', None),
                    
                    # Rushing
                    'rush_yd': player_stats.get('rush_yd', None),
                    'rush_td': player_stats.get('rush_td', None),
                    'rush_att': player_stats.get('rush_att', None),
                    
                    # Receiving  
                    'rec': player_stats.get('rec', None),
                    'rec_yd': player_stats.get('rec_yd', None),
                    'rec_td': player_stats.get('rec_td', None),
                    'rec_tgt': player_stats.get('rec_tgt', None),
                    
                    # Kicking
                    'fgm': player_stats.get('fgm', None),
                    'fga': player_stats.get('fga', None),
                    'xpm': player_stats.get('xpm', None),
                    'xpa': player_stats.get('xpa', None),
                    
                    # Defense
                    'def_int': player_stats.get('def_int', None),
                    'def_sack': player_stats.get('def_sack', None),
                    'def_td': player_stats.get('def_td', None),
                    'pts_allow': player_stats.get('pts_allow', None),
                    
                    # Misc
                    'fum_lost': player_stats.get('fum_lost', None),
                }
                
                all_player_data.append({
                    'year': year,
                    'week': week,
                    'team_name': team_name,
                    'roster_id': roster_id,
                    'player_id': player_id,
                    'player_name': f"{player_info.get('first_name', '')} {player_info.get('last_name', '')}".strip() or player_id,
                    'position': player_info.get('position', 'Unknown'),
                    'nfl_team': player_info.get('team', 'FA'),
                    'is_starter': is_starter,
                    'fantasy_points': fantasy_points,
                    **stats_dict  # Add all stats columns
                })
    
    return pd.DataFrame(all_player_data)