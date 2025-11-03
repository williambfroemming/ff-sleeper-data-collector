"""
Playoff Matchup Data Collector
Collects playoff bracket and matchup information
Outputs to: auto_stg_playoff_matchup_data
"""

from typing import Dict, List
import pandas as pd
from utils.api import get_playoff_bracket, get_matchups

def collect_playoff_matchup_data(
    league_id: str,
    year: int,
    playoff_weeks: List[int],
    week_to_round: Dict[int, int],
    rosters: List[dict],
    users: List[dict],
    name_map: Dict
) -> pd.DataFrame:
    """
    Collect playoff matchup data with consistent member IDs.

    Returns a DataFrame with columns:
      week (int), round (int), matchup_id (int),
      member_id (int), opponent_team_id (int),
      points (float), opponent_points (float)
    """
    print("  Collecting playoff matchup data...")

    # Build roster_id -> member_id mapping (same as regular_season.py)
    user_display_names = {entry['user_id']: entry['display_name'] for entry in users}
    
    roster_to_member = {}
    for roster in rosters:
        owner_id = roster.get("owner_id")
        if owner_id:
            display_name = user_display_names.get(owner_id)
            if display_name:
                member_id = int(name_map.get(display_name, display_name))
                roster_to_member[roster['roster_id']] = member_id

    # Bracket fetch retained in case you still want additional validation/filtering later
    _ = get_playoff_bracket(league_id)

    rows = []

    for week in playoff_weeks:
        matchups = get_matchups(league_id, week)
        if not matchups:
            continue

        # Group by matchup_id to reliably find opponents
        by_mid: Dict[int, List[dict]] = {}
        for m in matchups:
            mid = m.get("matchup_id")
            if mid is None:
                continue
            by_mid.setdefault(int(mid), []).append(m)

        round_number = int(week_to_round.get(week, 0))

        for mid, group in by_mid.items():
            if len(group) < 1:
                continue

            if len(group) == 1:
                a = group[0]
                roster_id = a["roster_id"]
                member_id = roster_to_member.get(roster_id)
                if member_id is None:
                    continue
                    
                rows.append({
                    "week": int(week),
                    "round": round_number,
                    "matchup_id": int(mid),
                    "member_id": member_id,
                    "opponent_team_id": None,
                    "points": float(a.get("points", 0.0) or 0.0),
                    "opponent_points": None,
                })
                continue

            # len(group) >= 2: pair them
            for i in range(0, len(group), 2):
                a = group[i]
                b = group[i + 1] if i + 1 < len(group) else None

                a_roster_id = a["roster_id"]
                a_member = roster_to_member.get(a_roster_id)
                a_points = float(a.get("points", 0.0) or 0.0)
                
                if a_member is None:
                    continue

                if b is not None:
                    b_roster_id = b["roster_id"]
                    b_member = roster_to_member.get(b_roster_id)
                    b_points = float(b.get("points", 0.0) or 0.0)
                    
                    if b_member is None:
                        continue

                    # Row for team A
                    rows.append({
                        "week": int(week),
                        "round": round_number,
                        "matchup_id": int(mid),
                        "member_id": a_member,
                        "opponent_team_id": b_member,
                        "points": a_points,
                        "opponent_points": b_points,
                    })
                    # Row for team B
                    rows.append({
                        "week": int(week),
                        "round": round_number,
                        "matchup_id": int(mid),
                        "member_id": b_member,
                        "opponent_team_id": a_member,
                        "points": b_points,
                        "opponent_points": a_points,
                    })
                else:
                    # No opponent record
                    rows.append({
                        "week": int(week),
                        "round": round_number,
                        "matchup_id": int(mid),
                        "member_id": a_member,
                        "opponent_team_id": None,
                        "points": a_points,
                        "opponent_points": None,
                    })

    df = pd.DataFrame.from_records(rows, columns=[
        "week", "round", "matchup_id",
        "member_id", "opponent_team_id", "points", "opponent_points"
    ])

    if df.empty:
        return df

    df = df[~df['matchup_id'].isin([5, 7])]

    # Enforce stable dtypes
    int_cols = ["week", "round", "matchup_id", "member_id", "opponent_team_id"]
    for c in int_cols:
        if c in df.columns:
            df[c] = df[c].fillna(-1).astype("int64")

    for c in ["points", "opponent_points"]:
        if c in df.columns:
            df[c] = df[c].fillna(0.0).astype("float64")

    return df