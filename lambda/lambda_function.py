"""
Fantasy Football Data Ingest Lambda
Collects data from Sleeper API and writes to S3 Data Lake

Table Mappings:
- stg_regular_season          <- regular_season.py
- stg_matchup_data            <- matchup_data.py
- stg_playoff_matchup_data    <- playoff_matchup_data.py
- stg_player_details_by_team  <- player_details_by_team.py
- stg_player_total_points     <- player_total_points.py

Manual Tables (NOT collected):
- stg_member
- stg_auction_draft
- stg_lineup_efficiency_weekly
"""

import json
import os
import boto3
import pandas as pd
from datetime import datetime
from io import BytesIO
import traceback

# Import collectors
from collectors.regular_season import collect_regular_season_data
from collectors.matchup_data import collect_matchup_data
from collectors.playoff_matchup_data import collect_playoff_matchup_data
from collectors.player_details_by_team import collect_player_details_by_team_data
from collectors.player_total_points import collect_player_total_points_data

# Import utilities
from utils.api import get_league_rosters, get_league_users, get_nfl_state
from utils.mappings import create_mappings


# Configuration
CURRENT_LEAGUE_ID = os.environ.get('CURRENT_LEAGUE_ID')
CURRENT_YEAR = int(os.environ.get('CURRENT_YEAR', datetime.now().year))
HISTORICAL_LEAGUES = json.loads(os.environ.get('HISTORICAL_LEAGUES', '{}'))
LAKE_BUCKET = os.environ.get('LAKE_BUCKET')
NAME_MAP = json.loads(os.environ.get('NAME_MAP', '{}'))
SCORING_SETTINGS = json.loads(os.environ.get('SCORING_SETTINGS', '{}'))

s3_client = boto3.client('s3')


def write_to_s3(df: pd.DataFrame, table_name: str, year: int):
    """
    Write DataFrame to S3 as year-partitioned Parquet.
    Overwrites existing file for that year.
    
    Args:
        df: DataFrame to write
        table_name: Name of the table (e.g., 'stg_regular_season')
        year: Year for partitioning
    """
    if df.empty:
        print(f"  WARNING: Skipping {table_name} - no data to write")
        return
    
    # Construct S3 path with year partition
    s3_key = f"staging/{table_name}/year={year}/data.parquet"
    
    # Convert to parquet in memory
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    parquet_buffer.seek(0)
    
    # Upload to S3
    try:
        s3_client.put_object(
            Bucket=LAKE_BUCKET,
            Key=s3_key,
            Body=parquet_buffer.getvalue()
        )
        print(f"  SUCCESS: Wrote {len(df)} rows to s3://{LAKE_BUCKET}/{s3_key}")
    except Exception as e:
        print(f"  ERROR: Failed to write to S3: {e}")
        raise


def get_current_week():
    """Get current NFL week from Sleeper API."""
    nfl_state = get_nfl_state()
    return nfl_state.get('week', 1)


def collect_season_data(league_id: str, year: int, week: int = None, 
                        collect_playoffs: bool = False,
                        collect_player_totals: bool = False):
    """
    Collect data for a specific season.
    
    Args:
        league_id: Sleeper league ID
        year: Season year
        week: Current week (if None, will fetch from API for current year only)
        collect_playoffs: Whether to collect playoff data
        collect_player_totals: Whether to collect player total points
    """
    print(f"\n{'='*60}")
    print(f"Collecting data for {year} season")
    print(f"League ID: {league_id}")
    print(f"{'='*60}\n")
    
    # Get current week if not provided (only for current year)
    if week is None and year == CURRENT_YEAR:
        week = get_current_week()
    elif week is None:
        # For historical years, assume full season
        week = 17
    
    print(f"Collecting through week: {week}")
    
    # Fetch league info
    print("\nFetching league info...")
    rosters = get_league_rosters(league_id)
    users = get_league_users(league_id)
    
    if not rosters or not users:
        raise Exception(f"Failed to fetch league rosters or users for {year}")
    
    # Create mappings
    roster_to_owner, owner_to_display, owner_to_user_id = create_mappings(rosters, users)
    
    # Define week ranges
    regular_season_weeks = range(1, min(week + 1, 15))  # Weeks 1-14
    playoff_weeks = [w for w in range(15, min(week + 1, 18))]  # Weeks 15-17
    
    results = {}
    
    try:
        # 1. Regular Season Standings
        print("\n[1/5] Regular Season Standings")
        df_regular_season = collect_regular_season_data(
            league_id, year, rosters, users, NAME_MAP
        )
        write_to_s3(df_regular_season, 'stg_regular_season', year)
        results['stg_regular_season'] = len(df_regular_season)
        
        # 2. Weekly Matchup Data
        print("\n[2/5] Weekly Matchup Data")
        df_matchups = collect_matchup_data(
            league_id, year, regular_season_weeks,
            roster_to_owner, owner_to_display, NAME_MAP
        )
        write_to_s3(df_matchups, 'stg_matchup_data', year)
        results['stg_matchup_data'] = len(df_matchups)
        
        # 3. Player Details by Team
        print("\n[3/5] Player Details by Team")
        df_players = collect_player_details_by_team_data(
            league_id, year, regular_season_weeks,
            roster_to_owner, owner_to_display, NAME_MAP, SCORING_SETTINGS
        )
        write_to_s3(df_players, 'stg_player_details_by_team', year)
        results['stg_player_details_by_team'] = len(df_players)
        
        # 4. Playoff Matchup Data (only if requested or playoffs have started)
        if collect_playoffs or playoff_weeks:
            print("\n[4/5] Playoff Matchup Data")
            if playoff_weeks:
                week_to_round = {15: 1, 16: 2, 17: 3}
                df_playoffs = collect_playoff_matchup_data(
                    league_id, year, playoff_weeks, week_to_round,
                    roster_to_owner, owner_to_display, NAME_MAP
                )
                write_to_s3(df_playoffs, 'stg_playoff_matchup_data', year)
                results['stg_playoff_matchup_data'] = len(df_playoffs)
            else:
                print("  SKIPPED: No playoff weeks yet")
        else:
            print("\n[4/5] Playoff Matchup Data - SKIPPED")
        
        # 5. Player Total Points (only if requested)
        if collect_player_totals:
            print("\n[5/5] Player Total Points")
            df_totals = collect_player_total_points_data([year], SCORING_SETTINGS)
            write_to_s3(df_totals, 'stg_player_total_points', year)
            results['stg_player_total_points'] = len(df_totals)
        else:
            print("\n[5/5] Player Total Points - SKIPPED")
        
    except Exception as e:
        print(f"\nERROR: Error collecting data for {year}: {e}")
        traceback.print_exc()
        raise
    
    return results


def handler(event, context):
    """
    Lambda handler function.
    
    Event parameters:
        - backfill_historical: (bool) If true, collect all historical years
        - year: (int) Specific year to collect
        - league_id: (str) Override league ID for specific year
        - week: (int) Override current week
        - collect_playoffs: (bool) Force playoff collection
        - collect_player_totals: (bool) Force player totals collection
    """
    print(f"Lambda invoked at: {datetime.utcnow().isoformat()}")
    print(f"Event: {json.dumps(event, default=str)}")
    
    try:
        all_results = {}
        
        # Historical backfill mode
        if event.get('backfill_historical'):
            print("\n" + "="*60)
            print("HISTORICAL BACKFILL MODE")
            print("="*60)
            
            for year_str, league_id in HISTORICAL_LEAGUES.items():
                year = int(year_str)
                print(f"\nProcessing historical year: {year}")
                results = collect_season_data(
                    league_id, 
                    year, 
                    week=17,  # Full season
                    collect_playoffs=True,
                    collect_player_totals=True
                )
                all_results[year] = results
            
            print("\n" + "="*60)
            print("HISTORICAL BACKFILL COMPLETE")
            print("="*60)
            
        # Single year collection mode
        else:
            year = event.get('year', CURRENT_YEAR)
            league_id = event.get('league_id', CURRENT_LEAGUE_ID)
            week = event.get('week')
            collect_playoffs = event.get('collect_playoffs', False)
            collect_player_totals = event.get('collect_player_totals', False)
            
            if not league_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'CURRENT_LEAGUE_ID not configured'})
                }
            
            results = collect_season_data(
                league_id, 
                year, 
                week,
                collect_playoffs,
                collect_player_totals
            )
            all_results[year] = results
        
        print(f"\n{'='*60}")
        print("DATA COLLECTION COMPLETE")
        print(f"{'='*60}\n")
        print("Summary:")
        for year, results in all_results.items():
            print(f"\nYear {year}:")
            for table, count in results.items():
                print(f"  {table}: {count} rows")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data collection successful',
                'results': all_results,
                'timestamp': datetime.utcnow().isoformat()
            }, default=str)
        }
        
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'traceback': traceback.format_exc()
            })
        }


if __name__ == "__main__":
    # For local testing
    test_event = {
        'year': 2025
    }
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
