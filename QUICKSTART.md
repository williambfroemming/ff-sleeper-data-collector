# Quick Start Guide

Get up and running in 5 minutes! ⚡

## TL;DR

```bash
# 1. Clone and enter directory
git clone https://github.com/yourusername/fantasy-football-sleeper.git
cd fantasy-football-sleeper

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp examples/example_config.py config.py
# Edit config.py with your league ID and settings

# 5. Run!
python main.py
```

## What You Need

1. **Your Sleeper League ID**
   - Go to your league on Sleeper
   - Look at URL: `https://sleeper.com/leagues/YOUR_LEAGUE_ID`
   - Copy that long number

2. **Where to save files**
   - Pick a folder on your computer (e.g., `/Users/yourname/Desktop/Fantasy`)

3. **League member usernames**
   - The Sleeper usernames of everyone in your league

## 3-Minute Setup

### 1. Get the Code
Download the ZIP from GitHub or clone it:
```bash
git clone https://github.com/yourusername/fantasy-football-sleeper.git
```

### 2. Set Up Python Environment
```bash
cd fantasy-football-sleeper
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Your League
```bash
cp examples/example_config.py config.py
```

Edit `config.py`:
```python
LEAGUE_IDS = ['YOUR_LEAGUE_ID_HERE']
START_YEAR = 2024
BASE_OUTPUT_DIR = '/path/to/your/output/folder'

NAME_MAP = {
    "sleeper_username": "Real Name",
    # ... add your league members
}
```

### 4. Run It!
```bash
python main.py
```

Your Excel files will be in your `BASE_OUTPUT_DIR`!

## VS Code Users

For detailed VS Code setup, see [VSCODE_SETUP.md](VSCODE_SETUP.md)

Quick version:
1. Open folder in VS Code
2. Install Python extension
3. Select Python interpreter from `venv`
4. Press F5 to run

## What You Get

Five types of Excel files:
- **League Standings** - Final W/L/Points
- **Weekly Matchups** - All matchup data
- **Playoff Data** - Playoff bracket results
- **High/Low Points** - Weekly top/bottom scorers
- **Player Details** - Individual player stats (optional)

Plus a combined file with everything!

## Troubleshooting

**"config.py not found"**
→ Copy `examples/example_config.py` to `config.py`

**"Module not found"**
→ Activate venv and run `pip install -r requirements.txt`

**Script is slow**
→ In `main.py`, set `COLLECT_PLAYER_DATA = False`

**Need more help?**
→ See [README.md](README.md) or [VSCODE_SETUP.md](VSCODE_SETUP.md)

## Next Steps

- Update `config.py` each season
- Customize scoring settings to match your league
- Disable data types you don't need for faster runs
- Set up to run automatically at season end

---

Questions? Open an issue on GitHub! 🏈
