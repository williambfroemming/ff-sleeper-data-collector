# Fantasy Football Data Collector - Project Summary

## 📁 Complete Project Structure

```
fantasy-football-sleeper/
├── README.md                    # Main documentation
├── QUICKSTART.md                # 5-minute setup guide
├── VSCODE_SETUP.md             # Detailed VS Code instructions
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── main.py                      # Main entry point - RUN THIS!
│
├── collectors/                  # Data collection modules
│   ├── __init__.py
│   ├── league_standings.py     # League standings collector
│   ├── matchups.py             # Weekly matchups collector
│   ├── playoffs.py             # Playoff data collector
│   ├── highlow.py              # High/low points collector
│   └── players.py              # Player details collector (slow)
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── api.py                  # Sleeper API wrapper
│   ├── mappings.py             # Name/roster mappings
│   └── scoring.py              # Fantasy point calculations
│
└── examples/
    └── example_config.py        # Configuration template
```

## 🎯 What This Does

Collects comprehensive fantasy football data from Sleeper's API and exports to Excel:

1. **League Standings** - Final season standings with W/L and points
2. **Weekly Matchups** - All regular season matchups with opponents
3. **Playoff Data** - Playoff bracket and results
4. **High/Low Points** - Weekly high and low scorers
5. **Player Details** - Individual player stats and fantasy points

## 🚀 Quick Start

```bash
# 1. Set up
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp examples/example_config.py config.py
# Edit config.py with your league info

# 3. Run
python main.py
```

## 📊 Output Files

### Individual Files (matches your existing format):
- `{year}_League_Data.xlsx` - League standings
- `{year}_season_weekly_data_summary.xlsx` - Weekly matchups
- `{year}_playoff_matchups.xlsx` - Playoff results
- `{year}_HighLow_points_summary.xlsx` - Weekly highs/lows
- `{year}_player_details.xlsx` - Player-level data

### Combined File:
- `{year}_complete_fantasy_data.xlsx` - All data in one workbook

## 🔧 Configuration

Edit `config.py` with:

1. **League ID** - Find in Sleeper URL
2. **Season Year** - Current season
3. **Output Directory** - Where to save files
4. **Name Mappings** - Map Sleeper usernames to real names
5. **Scoring Settings** - Your league's scoring rules

## 💻 VS Code Usage

1. Open folder in VS Code
2. Install Python extension
3. Create virtual environment: `python3 -m venv venv`
4. Select Python interpreter (from venv)
5. Open integrated terminal (`` Ctrl+` ``)
6. Activate venv: `source venv/bin/activate`
7. Install requirements: `pip install -r requirements.txt`
8. Configure your `config.py`
9. Press F5 or run: `python main.py`

## 📝 Key Features

### Modular Design
- Each data type has its own collector module
- Can enable/disable collectors individually
- Reusable utility functions

### Error Handling
- Retry logic for API calls
- Graceful failure handling
- Clear error messages

### Flexible Output
- Individual files (matches existing format)
- Combined file (all data in one place)
- Multiple sheets in combined file

### Performance Options
- Skip player data collection for speed
- Rate limit protection
- Efficient data reuse

## 🎛️ Customization

### Toggle Data Collection
Edit flags in `main.py`:
```python
COLLECT_LEAGUE_DATA = True
COLLECT_MATCHUP_DATA = True
COLLECT_PLAYOFF_DATA = True
COLLECT_HIGHLOW_DATA = True
COLLECT_PLAYER_DATA = False  # Slow - set to False to skip
```

### Change Output Format
Edit `SAVE_INDIVIDUAL_FILES` and `SAVE_COMBINED_FILE`.

### Adjust Scoring
Edit `SCORING_SETTINGS` in `config.py` to match your league.

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - Get running in 5 minutes
- **VSCODE_SETUP.md** - Detailed VS Code setup
- **examples/example_config.py** - Configuration template with comments

## 🔄 Workflow

1. **Setup** (once)
   - Clone repo
   - Create venv
   - Install dependencies
   - Configure

2. **Run** (annually)
   - Update config for new season
   - Run `python main.py`
   - Get Excel files

3. **Import** (to your database)
   - Files match your existing column structure
   - Ready to import to Excel sheets

## 🛠️ Tech Stack

- **Python 3.8+** - Main language
- **requests** - API calls
- **pandas** - Data manipulation
- **openpyxl** - Excel file creation

## 📦 Dependencies

```txt
requests>=2.31.0   # HTTP requests
pandas>=2.0.0      # Data analysis
openpyxl>=3.1.0    # Excel files
```

## 🤝 GitHub Ready

This project is structured following Python best practices:

- **Modular architecture** - Easy to maintain
- **Clear separation of concerns** - Each module has one job
- **Documented** - Comments and docstrings
- **Configurable** - Settings in one file
- **Gitignore** - Excludes config and data files
- **License** - MIT (permissive)

## 🔐 Security

- Config file (with sensitive info) is gitignored
- Example config provided instead
- No hardcoded credentials
- Read-only API access

## 🎓 Learning Resources

- [Sleeper API Docs](https://docs.sleeper.app/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🐛 Troubleshooting

See README.md for common issues and solutions.

## 📈 Future Enhancements

Potential additions:
- Historical data across multiple seasons
- Advanced analytics and visualizations
- Web dashboard
- Automatic scheduling
- Draft data collection
- Transaction history

## 📄 License

MIT License - Free to use and modify

## 🏈 Use Cases

- End-of-season data collection
- Historical record keeping
- League analysis
- Trophy/award determination
- Year-over-year comparisons
- Settling arguments with data!

---

**Ready to get started?** See [QUICKSTART.md](QUICKSTART.md)

**Need help with VS Code?** See [VSCODE_SETUP.md](VSCODE_SETUP.md)

**Questions?** Check [README.md](README.md) or open an issue on GitHub
