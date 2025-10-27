# Fantasy Football Data Collector (Sleeper API)

A comprehensive Python tool to collect and analyze fantasy football data from Sleeper's API. Exports data to Excel for easy analysis and record-keeping.

## Features

- **League Standings**: Final standings with wins, losses, points for/against
- **Weekly Matchups**: Complete regular season matchup data with opponents
- **Playoff Data**: Playoff bracket and matchup information
- **High/Low Points**: Weekly high and low scorers
- **Player Details**: Individual player statistics and fantasy points (optional)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### 1. Clone this repository
```bash
git clone https://github.com/yourusername/fantasy-football-sleeper.git
cd fantasy-football-sleeper
```

### 2. Create a virtual environment (recommended)
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Copy the example config
```bash
cp examples/example_config.py config.py
```

### 2. Edit config.py with your league information

**For a single season:**
```python
LEAGUE_IDS = ['your_2024_league_id']
START_YEAR = 2024
BASE_OUTPUT_DIR = '/path/to/your/output/folder'

NAME_MAP = {
    "sleeper_username1": "Real Name 1",
    "sleeper_username2": "Real Name 2",
    # ... add all your league members
}
```

**For multiple seasons (to collect historical data):**
```python
# List league IDs in chronological order (oldest first)
# Sleeper creates a new league ID each year for the same league
LEAGUE_IDS = [
    'your_2022_league_id',  # First year
    'your_2023_league_id',  # Second year
    'your_2024_league_id'   # Third year
]
START_YEAR = 2022  # Must match the year of your FIRST league ID

BASE_OUTPUT_DIR = '/path/to/your/output/folder'

NAME_MAP = {
    "sleeper_username1": "Real Name 1",
    # ... add all your league members
}
```

The script will automatically process each league ID as a separate year, creating files like:
- `2022_League_Data.xlsx`
- `2023_League_Data.xlsx`
- `2024_League_Data.xlsx`

### 3. Find your League ID(s)

**For current season:**
- Go to your league on Sleeper
- Look at the URL: `https://sleeper.com/leagues/YOUR_LEAGUE_ID`
- Copy the long number (e.g., `1124822672346198016`)

**For previous seasons (to collect historical data):**
- Log into Sleeper
- Click on your profile/avatar
- Go to "Leagues" tab
- You'll see your leagues by year
- Click into each past season's league
- Copy the league ID from the URL
- Add them to `LEAGUE_IDS` in chronological order (oldest first)

## Usage

### Run the complete data collection
```bash
python main.py
```

### Customize what to collect
Edit flags in `main.py`:
```python
COLLECT_LEAGUE_DATA = True
COLLECT_MATCHUP_DATA = True
COLLECT_PLAYOFF_DATA = True
COLLECT_HIGHLOW_DATA = True
COLLECT_PLAYER_DATA = True  # Set to False to skip (slower)
```

## VS Code Setup

### 1. Open in VS Code
- Open VS Code
- File -> Open Folder -> Select `fantasy-football-sleeper`

### 2. Install Python extension
- Click Extensions icon or press `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows)
- Search for "Python" by Microsoft
- Click Install

### 3. Set up Python environment
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
- Type "Python: Select Interpreter"
- Choose the interpreter from your `venv` folder

### 4. Run the script
- Open `main.py`
- Press `F5` or click the Run button
- Or use the integrated terminal: `python main.py`

### Using the Integrated Terminal
1. Open terminal: `` Ctrl+` `` or View -> Terminal
2. Activate virtual environment:
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```
3. Run: `python main.py`

## Output Files

The script creates separate Excel files in your configured output directories:

```
/Your/Output/Directory/
├── Annual_League_Data/
│   └── 2024_League_Data.xlsx
├── Annual_Matchup_Data/
│   └── 2024_season_weekly_data_summary.xlsx
├── Playoff_Data/
│   └── 2024_playoff_matchups.xlsx
├── Complete_Data/
│   ├── 2024_complete_fantasy_data.xlsx  (all data in one file)
│   └── 2024_player_details.xlsx
└── 2024_HighLow_points_summary.xlsx
```

## Project Structure

```
fantasy-football-sleeper/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config.py                    # Your configuration (create from example)
├── main.py                      # Main entry point
├── collectors/                  # Data collection modules
│   ├── __init__.py
│   ├── league_standings.py
│   ├── matchups.py
│   ├── playoffs.py
│   ├── highlow.py
│   └── players.py
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── api.py                  # Sleeper API wrapper
│   ├── mappings.py             # Name/roster mappings
│   └── scoring.py              # Fantasy point calculations
└── examples/
    └── example_config.py        # Example configuration
```

## Customization

### Scoring Settings

If your league uses custom scoring, edit the `SCORING_SETTINGS` in `config.py`:

```python
SCORING_SETTINGS = {
    'pass_yd': 0.04,      # 1 point per 25 yards
    'pass_td': 4,         # 4 points per passing TD
    'rush_yd': 0.1,       # 1 point per 10 yards
    # ... customize as needed
}
```

### Output Directories

Change where files are saved by editing `OUTPUT_DIRS` in `config.py`:

```python
OUTPUT_DIRS = {
    'league': f'{BASE_OUTPUT_DIR}/Annual_League_Data',
    'matchup': f'{BASE_OUTPUT_DIR}/Annual_Matchup_Data',
    # ... etc
}
```

## Troubleshooting

### "Module not found" error
- Make sure your virtual environment is activated
- Run `pip install -r requirements.txt` again

### "Failed to fetch data" error
- Check your internet connection
- Verify your league ID is correct
- Sleeper API may be rate-limiting (wait a minute and try again)

### Player data is slow
- This is normal. The player module fetches stats for every player every week
- Set `COLLECT_PLAYER_DATA = False` in `main.py` to skip this

### Empty Excel files
- Make sure the season has started and games have been played
- Check that your `START_YEAR` matches the current season

### "config.py not found"
- Make sure you copied `examples/example_config.py` to `config.py`
- Check that it's in the root directory (same level as `main.py`)

### Can't activate virtual environment (Windows PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## API Rate Limits

The Sleeper API recommends staying under 1000 calls per minute. This script:
- Implements retry logic with delays
- Reuses data where possible
- Should not exceed rate limits under normal usage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built using the [Sleeper API](https://docs.sleeper.app/)
- Inspired by the need to track fantasy football league history
