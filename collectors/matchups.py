"""
Weekly Matchup Data Collector
Collects all regular season matchup data with opponents and scores
"""

import pandas as pd
from typing import Dict, List
from utils.api import get_matchups
from utils.mappings import get_real_name


def collect_matchup_data(league_id: str, year: int, weeks: range,
                         roster_to_owner: Dict, owner_to_display: Dict, 
                         name_map: Dict) -> pd.DataFrame:
    """
    Collect weekly matchup data for regular season.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        weeks: Range of weeks to collect
        roster_to_owner: Mapping of roster_id -> owner_id
        owner_to_display: Mapping of owner_id -> display_name
        name_map: Mapping of display_name -> real_name
        
    Returns:
        DataFrame with weekly matchup data including opponents
    """
    print(f"  📅 Collecting weekly matchups...")
    
    all_data = []
    
    for week in weeks:
        matchups = get_matchups(league_id, week)
        if not matchups:
            continue
            
        for matchup in matchups:
            team_id = matchup['roster_id']
            matchup_id = matchup['matchup_id']
            points_scored = matchup['points']
            owner_id = roster_to_owner.get(team_id)
            real_name = get_real_name(owner_id, owner_to_display, name_map)

            all_data.append({
                'year': year,
                'week': week,
                'matchup_id': matchup_id,
                'team_id': real_name,
                'points_scored': points_scored,
            })
    
    df = pd.DataFrame(all_data)
    
    # Add opponent data
    df = _assign_opponents(df)
    
    return df


def _assign_opponents(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add opponent information to matchup data.
    Teams with the same matchup_id in the same week face each other.
    """
    df['opponent_team_id'] = None
    df['opponent_points'] = None

    def assign_opponent_data(group):
        if len(group) == 2:
            team1, team2 = group.iloc[0], group.iloc[1]
            group.loc[group.index[0], 'opponent_team_id'] = team2['team_id']
            group.loc[group.index[1], 'opponent_team_id'] = team1['team_id']
            group.loc[group.index[0], 'opponent_points'] = team2['points_scored']
            group.loc[group.index[1], 'opponent_points'] = team1['points_scored']
        return group

    return df.groupby(['week', 'matchup_id'], group_keys=False).apply(assign_opponent_data)
