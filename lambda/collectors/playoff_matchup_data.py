"""
Playoff Matchup Data Collector
Collects playoff bracket and matchup information
Outputs to: stg_playoff_matchup_data
"""

import pandas as pd
from typing import Dict, List
from utils.api import get_playoff_bracket, get_matchups
from utils.mappings import get_real_name


def collect_playoff_matchup_data(league_id: str, year: int, playoff_weeks: List[int],
                         week_to_round: Dict, roster_to_owner: Dict, 
                         owner_to_display: Dict, name_map: Dict) -> pd.DataFrame:
    """
    Collect playoff matchup data.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        playoff_weeks: List of playoff week numbers
        week_to_round: Mapping of week -> playoff round
        roster_to_owner: Mapping of roster_id -> owner_id
        owner_to_display: Mapping of owner_id -> display_name
        name_map: Mapping of display_name -> real_name
        
    Returns:
        DataFrame with playoff matchup data
    """
    print(f"  Collecting playoff matchup data...")
    
    playoff_bracket = get_playoff_bracket(league_id)
    if not playoff_bracket:
        print("    WARNING: No playoff bracket found")
        return pd.DataFrame()
    
    all_playoff_matchups = []

    for week in playoff_weeks:
        matchups = get_matchups(league_id, week)
        if not matchups:
            continue
            
        matchup_points = {matchup['roster_id']: matchup['points'] for matchup in matchups}
        round_number = week_to_round.get(week)

        for matchup in matchups:
            for bracket_match in playoff_bracket:
                if bracket_match['r'] == round_number and (
                    matchup['roster_id'] == bracket_match['t1'] or 
                    matchup['roster_id'] == bracket_match['t2']):
                    
                    owner_id = roster_to_owner.get(matchup['roster_id'], "Unknown")
                    opponent_roster_id = (
                        bracket_match['t2'] if matchup['roster_id'] == bracket_match['t1'] 
                        else bracket_match['t1']
                    )
                    opponent_owner_id = roster_to_owner.get(opponent_roster_id, "Unknown")

                    owner_name = get_real_name(owner_id, owner_to_display, name_map)
                    opponent_name = get_real_name(opponent_owner_id, owner_to_display, name_map)

                    owner_points = matchup_points.get(matchup['roster_id'], 0)
                    opponent_points = matchup_points.get(opponent_roster_id, 0)

                    all_playoff_matchups.append({
                        "Year": year,
                        "Week": week,
                        "Round": round_number,
                        "Matchup ID": matchup['matchup_id'],
                        "Display Name": owner_name,
                        "Opponent Display Name": opponent_name,
                        "Points": owner_points,
                        "Opponent Points": opponent_points
                    })
    
    df = pd.DataFrame(all_playoff_matchups)
    
    # Filter out consolation games
    if not df.empty:
        df = df[
            ~((df['Round'] == 2) & (df['Matchup ID'] == 3)) &
            ~((df['Round'] == 3) & (df['Matchup ID'] == 2))
        ]
    
    return df
