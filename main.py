"""
Fantasy Football Data Collector - Main Entry Point
Collects comprehensive fantasy football data from Sleeper API
"""

import os
import pandas as pd
from typing import Dict

# Import configuration
try:
    import config
except ImportError:
    print("❌ ERROR: config.py not found!")
    print("Please copy examples/example_config.py to config.py and customize it.")
    exit(1)

# Import utilities and collectors
from utils import (
    get_league_rosters,
    get_league_users,
    create_mappings
)

from collectors import (
    collect_league_standings,
    collect_matchup_data,
    collect_playoff_data,
    collect_highlow_data,
    collect_player_data
)


# ============================================================================
# CONFIGURATION FLAGS - Toggle what to collect
# ============================================================================

COLLECT_LEAGUE_DATA = True
COLLECT_MATCHUP_DATA = True
COLLECT_PLAYOFF_DATA = True
COLLECT_HIGHLOW_DATA = True
COLLECT_PLAYER_DATA = True  # Set to False to skip (slow!)

SAVE_INDIVIDUAL_FILES = False  # Set to True if you need separate files for each data type
SAVE_COMBINED_FILE = True      # Recommended: All data in one Excel file with multiple sheets


# ============================================================================
# FILE SAVING FUNCTIONS
# ============================================================================

def save_individual_files(league_data_df: pd.DataFrame, matchup_df: pd.DataFrame, 
                         playoff_df: pd.DataFrame, highlow_df: pd.DataFrame, 
                         player_df: pd.DataFrame, year: int):
    """Save data to individual files matching existing format."""
    print(f"\n  💾 Saving individual files...")
    
    # Create all output directories
    for dir_path in config.OUTPUT_DIRS.values():
        os.makedirs(dir_path, exist_ok=True)
    
    # 1. League Data
    if not league_data_df.empty:
        league_file = f"{config.OUTPUT_DIRS['league']}/{year}_League_Data.xlsx"
        league_data_df.to_excel(league_file, index=False)
        print(f"    ✓ League standings: {league_file}")
    
    # 2. Matchup Data
    if not matchup_df.empty:
        matchup_file = f"{config.OUTPUT_DIRS['matchup']}/{year}_season_weekly_data_summary.xlsx"
        matchup_df.to_excel(matchup_file, index=False)
        print(f"    ✓ Weekly matchups: {matchup_file}")
    
    # 3. Playoff Data
    if not playoff_df.empty:
        playoff_file = f"{config.OUTPUT_DIRS['playoff']}/{year}_playoff_matchups.xlsx"
        playoff_df.to_excel(playoff_file, index=False, sheet_name="Playoff Matchups")
        print(f"    ✓ Playoff data: {playoff_file}")
    
    # 4. High/Low Points
    if not highlow_df.empty:
        highlow_file = f"{config.OUTPUT_DIRS['highlow']}/{year}_HighLow_points_summary.xlsx"
        highlow_df.to_excel(highlow_file, index=False)
        print(f"    ✓ High/Low points: {highlow_file}")
    
    # 5. Player Data (if available)
    if not player_df.empty:
        player_file = f"{config.OUTPUT_DIRS['complete']}/{year}_player_details.xlsx"
        os.makedirs(config.OUTPUT_DIRS['complete'], exist_ok=True)
        player_df.to_excel(player_file, index=False)
        print(f"    ✓ Player details: {player_file}")


def save_combined_file(league_data_df: pd.DataFrame, matchup_df: pd.DataFrame, 
                      playoff_df: pd.DataFrame, highlow_df: pd.DataFrame, 
                      player_df: pd.DataFrame, year: int):
    """Save all data to one combined Excel file with multiple sheets."""
    print(f"\n  💾 Saving combined file...")
    
    combined_file = f"{config.OUTPUT_DIRS['complete']}/{year}_complete_fantasy_data.xlsx"
    os.makedirs(config.OUTPUT_DIRS['complete'], exist_ok=True)
    
    with pd.ExcelWriter(combined_file, engine='openpyxl') as writer:
        if not league_data_df.empty:
            league_data_df.to_excel(writer, sheet_name='League Standings', index=False)
        
        if not matchup_df.empty:
            matchup_df.to_excel(writer, sheet_name='Weekly Matchups', index=False)
        
        if not playoff_df.empty:
            playoff_df.to_excel(writer, sheet_name='Playoff Matchups', index=False)
        
        if not highlow_df.empty:
            highlow_df.to_excel(writer, sheet_name='High Low Points', index=False)
        
        if not player_df.empty:
            player_df.to_excel(writer, sheet_name='Player Details', index=False)
            
            # Add starters-only sheet
            starters_df = player_df[player_df['is_starter'] == True].copy()
            starters_df.to_excel(writer, sheet_name='Starters Only', index=False)
            
            # Add team summary
            if not matchup_df.empty:
                team_summary = matchup_df.groupby('team_id').agg({
                    'points_scored': ['sum', 'mean', 'max', 'min'],
                    'week': 'count'
                }).round(2)
                team_summary.columns = ['Total Points', 'Avg Points', 'Max Points', 
                                       'Min Points', 'Games']
                team_summary.to_excel(writer, sheet_name='Team Summary')
    
    print(f"    ✓ Combined file: {combined_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("=" * 80)
    print("FANTASY FOOTBALL DATA COLLECTOR")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  League IDs: {config.LEAGUE_IDS}")
    print(f"  Season Year: {config.START_YEAR}")
    print(f"  Output Directory: {config.BASE_OUTPUT_DIR}")
    print(f"\nData Collection:")
    print(f"  League Standings: {'✓' if COLLECT_LEAGUE_DATA else '✗'}")
    print(f"  Weekly Matchups: {'✓' if COLLECT_MATCHUP_DATA else '✗'}")
    print(f"  Playoff Data: {'✓' if COLLECT_PLAYOFF_DATA else '✗'}")
    print(f"  High/Low Points: {'✓' if COLLECT_HIGHLOW_DATA else '✗'}")
    print(f"  Player Details: {'✓' if COLLECT_PLAYER_DATA else '✗ (skipped for speed)'}")
    print()
    
    current_year = config.START_YEAR

    for league_id in config.LEAGUE_IDS:
        print("=" * 80)
        print(f"Processing league: {league_id}")
        print(f"Season: {current_year}")
        print("=" * 80)

        # Fetch base league data
        print("\n🔄 Fetching league information...")
        rosters = get_league_rosters(league_id)
        users = get_league_users(league_id)

        if not rosters or not users:
            print(f"❌ Failed to retrieve data for league {league_id}. Skipping...")
            current_year += 1
            continue

        roster_to_owner, owner_to_display, _ = create_mappings(rosters, users)
        print(f"✓ Found {len(rosters)} teams in the league")

        # Initialize dataframes
        league_data_df = pd.DataFrame()
        matchup_df = pd.DataFrame()
        playoff_df = pd.DataFrame()
        highlow_df = pd.DataFrame()
        player_df = pd.DataFrame()

        # Collect each type of data
        print("\n📥 Collecting data...")
        
        if COLLECT_LEAGUE_DATA:
            league_data_df = collect_league_standings(
                league_id, current_year, rosters, users, config.NAME_MAP
            )
        
        if COLLECT_MATCHUP_DATA:
            matchup_df = collect_matchup_data(
                league_id, current_year, config.REGULAR_SEASON_WEEKS,
                roster_to_owner, owner_to_display, config.NAME_MAP
            )
        
        if COLLECT_PLAYOFF_DATA:
            playoff_df = collect_playoff_data(
                league_id, current_year, config.PLAYOFF_WEEKS,
                config.WEEK_TO_ROUND, roster_to_owner, 
                owner_to_display, config.NAME_MAP
            )
        
        if COLLECT_HIGHLOW_DATA:
            highlow_df = collect_highlow_data(
                league_id, current_year, config.REGULAR_SEASON_WEEKS,
                roster_to_owner, owner_to_display, config.NAME_MAP
            )
        
        if COLLECT_PLAYER_DATA:
            player_df = collect_player_data(
                league_id, current_year, config.REGULAR_SEASON_WEEKS,
                roster_to_owner, owner_to_display, config.NAME_MAP,
                config.SCORING_SETTINGS
            )

        # Save files
        if SAVE_INDIVIDUAL_FILES:
            save_individual_files(
                league_data_df, matchup_df, playoff_df, 
                highlow_df, player_df, current_year
            )
        
        if SAVE_COMBINED_FILE:
            save_combined_file(
                league_data_df, matchup_df, playoff_df, 
                highlow_df, player_df, current_year
            )

        current_year += 1
        print()

    print("=" * 80)
    print("✅ DATA COLLECTION COMPLETE!")
    print("=" * 80)
    print(f"\nCheck your output directory: {config.BASE_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
