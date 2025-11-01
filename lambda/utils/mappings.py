"""
Mapping utilities for converting between IDs and names
"""

from typing import Dict, List, Tuple


def create_mappings(rosters: List[dict], users: List[dict]) -> Tuple[Dict, Dict, Dict]:
    """
    Create mappings from roster_id to owner_id and owner_id to names.
    
    Args:
        rosters: List of roster objects from Sleeper API
        users: List of user objects from Sleeper API
        
    Returns:
        Tuple of (roster_to_owner, owner_to_display, owner_to_user_id)
    """
    roster_to_owner = {roster["roster_id"]: roster["owner_id"] for roster in rosters}
    owner_to_display = {user["user_id"]: user["display_name"] for user in users}
    owner_to_user_id = {user["display_name"]: user["user_id"] for user in users}
    
    return roster_to_owner, owner_to_display, owner_to_user_id


def get_real_name(owner_id: str, owner_to_display: Dict, name_map: Dict) -> str:
    """
    Get the real name for an owner using the name map.
    
    Args:
        owner_id: Sleeper user ID
        owner_to_display: Mapping of user_id -> display_name
        name_map: Mapping of display_name -> real_name
        
    Returns:
        Real name from NAME_MAP, or display name if not found
    """
    display_name = owner_to_display.get(owner_id, "Unknown")
    return name_map.get(display_name, display_name)


def calculate_points_with_decimal(settings: dict, key: str = "fpts") -> float:
    """
    Calculate points with decimal values from Sleeper roster settings.
    Sleeper stores decimals separately (e.g., 123.45 is stored as fpts=123, fpts_decimal=45)
    
    Args:
        settings: Roster settings dict
        key: Base key name ('fpts' or 'fpts_against')
        
    Returns:
        Float value of points
    """
    if isinstance(settings, dict) and key in settings and f"{key}_decimal" in settings:
        return settings[key] + settings[f"{key}_decimal"] / 100
    return 0.0
