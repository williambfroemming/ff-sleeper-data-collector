"""
Example Configuration File
Copy this to config.py and customize with your league information
"""

# ============================================================================
# LEAGUE CONFIGURATION
# ============================================================================

# Your Sleeper League IDs (find in URL: sleeper.com/leagues/YOUR_LEAGUE_ID)
LEAGUE_IDS = [
    'YOUR_LEAGUE_ID_HERE'  # Replace with your actual league ID
]

# The year/season you want to collect data for
START_YEAR = 2024

# Week ranges
REGULAR_SEASON_WEEKS = range(1, 15)  # Weeks 1-14
PLAYOFF_WEEKS = [15, 16, 17]          # Weeks 15-17

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Base directory where all data will be saved
BASE_OUTPUT_DIR = '/path/to/your/output/folder'  # CHANGE THIS!

# Individual output directories (you can customize these)
OUTPUT_DIRS = {
    'league': f'{BASE_OUTPUT_DIR}/Annual_League_Data',
    'matchup': f'{BASE_OUTPUT_DIR}/Annual_Matchup_Data',
    'playoff': f'{BASE_OUTPUT_DIR}/Playoff_Data',
    'highlow': BASE_OUTPUT_DIR,
    'complete': f'{BASE_OUTPUT_DIR}/Complete_Data'
}

# ============================================================================
# MEMBER NAME MAPPING
# ============================================================================

# Map Sleeper usernames to real names
# Add all your league members here!
NAME_MAP = {
    "sleeper_username1": "Real Name 1",
    "sleeper_username2": "Real Name 2",
    "sleeper_username3": "Real Name 3",
    # Add more as needed...
}

# ============================================================================
# SCORING SETTINGS
# ============================================================================

# Your league's scoring settings
# Customize these to match your league rules
SCORING_SETTINGS = {
    # Passing
    'pass_yd': 0.04,           # Points per passing yard (25 yards = 1 pt)
    'pass_td': 4,              # Points per passing TD
    'pass_2pt': 2,             # Points per 2-pt conversion
    'pass_int': -2,            # Points per interception
    'pass_int_td': -1,         # Points per pick-6
    
    # Rushing
    'rush_yd': 0.1,            # Points per rushing yard (10 yards = 1 pt)
    'rush_td': 6,              # Points per rushing TD
    'rush_2pt': 2,             # Points per 2-pt conversion
    'rush_fd': 0.5,            # Points per first down
    
    # Receiving
    'rec_yd': 0.1,             # Points per receiving yard (10 yards = 1 pt)
    'rec_td': 6,               # Points per receiving TD
    'rec_2pt': 2,              # Points per 2-pt conversion
    'rec_fd': 0.5,             # Points per first down
    
    # Kicking
    'fgm_0_19': 3,             # Field goal 0-19 yards
    'fgm_20_29': 3,            # Field goal 20-29 yards
    'fgm_30_39': 3,            # Field goal 30-39 yards
    'fgm_40_49': 4,            # Field goal 40-49 yards
    'fgm_50p': 5,              # Field goal 50+ yards
    'xpm': 1,                  # Extra point made
    'fgmiss': -1,              # Field goal missed
    'xpmiss': -1,              # Extra point missed
    
    # Defense/Special Teams
    'def_td': 6,               # Defensive TD
    'def_st_td': 6,            # Special teams TD
    'def_int': 2,              # Interception
    'def_sack': 1,             # Sack
    'def_safe': 3,             # Safety
    'def_blk_kick': 2,         # Blocked kick
    'def_3_and_out': 0.5,      # 3 and out
    'def_4_down_stop': 0.5,    # 4th down stop
    'def_st_fum_rec': 2,       # Special teams fumble recovery
    'def_st_ff': 1,            # Special teams forced fumble
    'def_fum_rec': 2,          # Fumble recovery
    'fum_rec_td': 6,           # Fumble recovery TD
    
    # Defense Points Allowed
    'pts_allow_0': 11,         # 0 points allowed
    'pts_allow_1_6': 8,        # 1-6 points allowed
    'pts_allow_7_13': 5,       # 7-13 points allowed
    'pts_allow_14_20': 2,      # 14-20 points allowed
    'pts_allow_21_27': 0,      # 21-27 points allowed
    'pts_allow_28_34': -2,     # 28-34 points allowed
    'pts_allow_35p': -5,       # 35+ points allowed
    
    # Fumbles
    'fum_lost': -2,            # Fumble lost
    
    # Bonuses
    'bonus_rush_yd_100': 2,    # 100-199 yard rushing game bonus
    'bonus_rush_yd_200': 4,    # 200+ yard rushing game bonus
    'bonus_rec_yd_100': 2,     # 100-199 yard receiving game bonus
    'bonus_rec_yd_200': 4,     # 200+ yard receiving game bonus
    'bonus_pass_yd_300': 2,    # 300-399 yard passing game bonus
    'bonus_pass_yd_400': 4,    # 400+ yard passing game bonus
}

# ============================================================================
# PLAYOFF CONFIGURATION
# ============================================================================

# Mapping of week number to playoff round
WEEK_TO_ROUND = {
    15: 1,  # Round 1
    16: 2,  # Round 2 (Semi-finals)
    17: 3   # Round 3 (Championship)
}
