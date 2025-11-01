"""
Sleeper API wrapper functions
Handles all API calls to Sleeper with retry logic and error handling
"""

import requests
import time
from typing import Dict, List, Optional


def fetch_data(url: str, retry_count: int = 3) -> Optional[Dict]:
    """
    Fetch data from Sleeper API with retry logic.
    
    Args:
        url: The API endpoint URL
        retry_count: Number of retry attempts
        
    Returns:
        JSON response as dict, or None if failed
    """
    for attempt in range(retry_count):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt < retry_count - 1:
                print(f"  Retry {attempt + 1}/{retry_count} for {url}")
                time.sleep(1)
            else:
                print(f"  Failed to fetch: {url}")
                print(f"  Error: {e}")
                return None


def get_league_rosters(league_id: str) -> List[Dict]:
    """Get all rosters in a league."""
    url = f'https://api.sleeper.app/v1/league/{league_id}/rosters'
    return fetch_data(url) or []


def get_league_users(league_id: str) -> List[Dict]:
    """Get all users in a league."""
    url = f'https://api.sleeper.app/v1/league/{league_id}/users'
    return fetch_data(url) or []


def get_matchups(league_id: str, week: int) -> List[Dict]:
    """Get matchups for a specific week."""
    url = f'https://api.sleeper.app/v1/league/{league_id}/matchups/{week}'
    return fetch_data(url) or []


def get_playoff_bracket(league_id: str) -> List[Dict]:
    """Get the winners bracket for playoffs."""
    url = f'https://api.sleeper.app/v1/league/{league_id}/winners_bracket'
    return fetch_data(url) or []


def get_all_players() -> Dict[str, Dict]:
    """
    Get all NFL players from Sleeper.
    This is a large (~5MB) response, so use sparingly.
    
    Returns:
        Dictionary of player_id -> player_info
    """
    print("  Fetching player database (~5MB, this may take a moment)...")
    url = 'https://api.sleeper.app/v1/players/nfl'
    players = fetch_data(url)
    
    if players:
        print(f"  Loaded {len(players)} players")
    return players or {}


def get_weekly_stats(year: int, week: int) -> Dict[str, Dict]:
    """
    Get weekly stats for all players.
    
    Args:
        year: Season year
        week: Week number
        
    Returns:
        Dictionary of player_id -> stats
    """
    url = f"https://api.sleeper.com/stats/nfl/{year}/{week}?season_type=regular"
    stats = fetch_data(url)
    
    # The API returns a list, convert to dict keyed by player_id
    if isinstance(stats, list):
        stats_dict = {}
        for player_stat in stats:
            if isinstance(player_stat, dict) and 'player_id' in player_stat:
                player_id = player_stat['player_id']
                stats_dict[player_id] = player_stat.get('stats', player_stat)
        return stats_dict
    elif isinstance(stats, dict):
        return stats
    else:
        return {}


def get_nfl_state() -> Dict:
    """Get current NFL season state."""
    url = 'https://api.sleeper.app/v1/state/nfl'
    return fetch_data(url) or {}
