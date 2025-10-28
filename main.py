"""
Fantasy Football Data Collector - Main Entry Point
Collects comprehensive fantasy football data from Sleeper API
Creates ONE combined file with all years
"""

import os
import pandas as pd

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

try:
    from collectors.historical_totals import collect_historical_player_totals
    HISTORICAL_TOTALS_AVAILABLE = True
except ImportError:
    HISTORICAL_TOTALS_AVAILABLE = False

try:
    from collectors.auction_draft import (
        collect_draft_analysis,
        calculate_team_draft_summary,
        calculate_positional_spending
    )
    DRAFT_ANALYSIS_AVAILABLE = True
except ImportError:
    DRAFT_ANALYSIS_AVAILABLE = False


# ============================================================================
# CONFIGURATION FLAGS - Toggle what to collect
# ============================================================================

COLLECT_LEAGUE_DATA = True
COLLECT_MATCHUP_DATA = True
COLLECT_PLAYOFF_DATA = True
COLLECT_HIGHLOW_DATA = True
COLLECT_PLAYER_DATA = True  # Set to False to skip (slow!)
COLLECT_DRAFT_ANALYSIS = False  # Requires draft data file
COLLECT_HISTORICAL_TOTALS = True  # Creates lookup table for draft value analysis

# Path to your draft data Excel file (set to None to skip draft analysis)
DRAFT_DATA_FILE = None  # e.g., '/path/to/AllTimeDraftData.xlsx'


# ============================================================================
# FILE SAVING FUNCTION
# ============================================================================

def save_combined_file(league_data_df, matchup_df, playoff_df, highlow_df, 
                      player_df, draft_analysis_df, team_draft_summary_df, 
                      position_spending_df, historical_totals_df, 
                      first_year, last_year):
    """Save all data to one combined Excel file with multiple sheets."""
    print(f"\n💾 Saving combined file...")
    
    filename = f"{first_year}-{last_year}_complete_fantasy_data.xlsx"
    combined_file = f"{config.OUTPUT_DIRS['complete']}/{filename}"
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
                team_summary = matchup_df.groupby(['year', 'team_id']).agg({
                    'points_scored': ['sum', 'mean', 'max', 'min'],
                    'week': 'count'
                }).round(2)
                team_summary.columns = ['Total Points', 'Avg Points', 'Max Points', 
                                       'Min Points', 'Games']
                team_summary.to_excel(writer, sheet_name='Team Summary')
        
        # Add historical player totals (for draft VLOOKUP)
        if not historical_totals_df.empty:
            historical_totals_df.to_excel(writer, sheet_name='Historical Player Totals', index=False)
        
        # Add draft analysis sheets
        if not draft_analysis_df.empty:
            draft_analysis_df.to_excel(writer, sheet_name='Draft Value Analysis', index=False)
            
        if not team_draft_summary_df.empty:
            team_draft_summary_df.to_excel(writer, sheet_name='Team Draft Summary', index=False)
            
        if not position_spending_df.empty:
            position_spending_df.to_excel(writer, sheet_name='Position Spending', index=False)
    
    print(f"✓ Saved: {combined_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("=" * 80)
    print("FANTASY FOOTBALL DATA COLLECTOR")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  League IDs: {len(config.LEAGUE_IDS)} leagues")
    print(f"  Years: {config.START_YEAR}-{config.START_YEAR + len(config.LEAGUE_IDS) - 1}")
    print(f"  Output Directory: {config.BASE_OUTPUT_DIR}")
    print(f"\nData Collection:")
    print(f"  League Standings: {'Yes' if COLLECT_LEAGUE_DATA else 'No'}")
    print(f"  Weekly Matchups: {'Yes' if COLLECT_MATCHUP_DATA else 'No'}")
    print(f"  Playoff Data: {'Yes' if COLLECT_PLAYOFF_DATA else 'No'}")
    print(f"  High/Low Points: {'Yes' if COLLECT_HIGHLOW_DATA else 'No'}")
    print(f"  Player Details: {'Yes' if COLLECT_PLAYER_DATA else 'No'}")
    print(f"  Historical Totals: {'Yes' if COLLECT_HISTORICAL_TOTALS else 'No'}")
    print()
    
    # Calculate years to collect
    years_to_collect = list(range(config.START_YEAR, config.START_YEAR + len(config.LEAGUE_IDS)))
    
    # Collect historical player totals ONCE
    historical_totals_df = pd.DataFrame()
    if COLLECT_HISTORICAL_TOTALS and HISTORICAL_TOTALS_AVAILABLE:
        historical_totals_df = collect_historical_player_totals(
            years_to_collect,
            config.SCORING_SETTINGS
        )
    
    # Accumulate data from all years
    all_league_data = []
    all_matchup_data = []
    all_playoff_data = []
    all_highlow_data = []
    all_player_data = []
    
    current_year = config.START_YEAR

    for league_id in config.LEAGUE_IDS:
        print("=" * 80)
        print(f"Processing: {current_year} (League ID: {league_id})")
        print("=" * 80)

        # Fetch base league data
        rosters = get_league_rosters(league_id)
        users = get_league_users(league_id)

        if not rosters or not users:
            print(f"❌ Failed to retrieve data. Skipping {current_year}...")
            current_year += 1
            continue

        roster_to_owner, owner_to_display, _ = create_mappings(rosters, users)
        print(f"✓ Found {len(rosters)} teams")

        # Collect each type of data
        if COLLECT_LEAGUE_DATA:
            df = collect_league_standings(league_id, current_year, rosters, users, config.NAME_MAP)
            if not df.empty:
                all_league_data.append(df)
        
        if COLLECT_MATCHUP_DATA:
            df = collect_matchup_data(league_id, current_year, config.REGULAR_SEASON_WEEKS,
                                     roster_to_owner, owner_to_display, config.NAME_MAP)
            if not df.empty:
                all_matchup_data.append(df)
        
        if COLLECT_PLAYOFF_DATA:
            df = collect_playoff_data(league_id, current_year, config.PLAYOFF_WEEKS,
                                     config.WEEK_TO_ROUND, roster_to_owner, 
                                     owner_to_display, config.NAME_MAP)
            if not df.empty:
                all_playoff_data.append(df)
        
        if COLLECT_HIGHLOW_DATA:
            df = collect_highlow_data(league_id, current_year, config.REGULAR_SEASON_WEEKS,
                                     roster_to_owner, owner_to_display, config.NAME_MAP)
            if not df.empty:
                all_highlow_data.append(df)
        
        if COLLECT_PLAYER_DATA:
            df = collect_player_data(league_id, current_year, config.REGULAR_SEASON_WEEKS,
                                    roster_to_owner, owner_to_display, config.NAME_MAP,
                                    config.SCORING_SETTINGS)
            if not df.empty:
                all_player_data.append(df)

        current_year += 1

    # Combine all years
    print("\n" + "=" * 80)
    print("Combining all years...")
    combined_league_data = pd.concat(all_league_data, ignore_index=True) if all_league_data else pd.DataFrame()
    combined_matchup_data = pd.concat(all_matchup_data, ignore_index=True) if all_matchup_data else pd.DataFrame()
    combined_playoff_data = pd.concat(all_playoff_data, ignore_index=True) if all_playoff_data else pd.DataFrame()
    combined_highlow_data = pd.concat(all_highlow_data, ignore_index=True) if all_highlow_data else pd.DataFrame()
    combined_player_data = pd.concat(all_player_data, ignore_index=True) if all_player_data else pd.DataFrame()

    # Save single combined file
    first_year = config.START_YEAR
    last_year = config.START_YEAR + len(config.LEAGUE_IDS) - 1
    
    save_combined_file(
        combined_league_data, combined_matchup_data, combined_playoff_data, 
        combined_highlow_data, combined_player_data, pd.DataFrame(),
        pd.DataFrame(), pd.DataFrame(), historical_totals_df,
        first_year, last_year
    )

    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"File: {first_year}-{last_year}_complete_fantasy_data.xlsx")
    print(f"Location: {config.OUTPUT_DIRS['complete']}")


if __name__ == "__main__":
    main()
