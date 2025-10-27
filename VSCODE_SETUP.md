# VS Code Setup Guide

Complete guide to running this project in Visual Studio Code on your local machine.

## Prerequisites

1. **Python 3.8+** installed on your system
   - Check: Open terminal and run `python --version` or `python3 --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **Visual Studio Code** installed
   - Download: [code.visualstudio.com](https://code.visualstudio.com/)

3. **Git** (for cloning the repository)
   - Download: [git-scm.com](https://git-scm.com/)

## Step-by-Step Setup

### 1. Clone or Download the Project

**Option A: Using Git (Recommended)**
```bash
# Open Terminal (Mac) or Command Prompt (Windows)
cd ~/Desktop  # Or wherever you want the project
git clone https://github.com/yourusername/fantasy-football-sleeper.git
cd fantasy-football-sleeper
```

**Option B: Download ZIP**
- Download the ZIP from GitHub
- Extract to your desired location
- Remember the path to the extracted folder

### 2. Open Project in VS Code

1. Launch VS Code
2. `File` → `Open Folder...`
3. Navigate to and select the `fantasy-football-sleeper` folder
4. Click "Open" or "Select Folder"

### 3. Install Python Extension

1. Click the Extensions icon in the sidebar (or press `Cmd+Shift+X` on Mac / `Ctrl+Shift+X` on Windows)
2. Search for "Python"
3. Install the extension by Microsoft (the one with millions of downloads)
4. Restart VS Code if prompted

### 4. Create Virtual Environment

**Open the integrated terminal in VS Code:**
- `` Ctrl+` `` (backtick) or `View` → `Terminal`

**Create the virtual environment:**

**On macOS/Linux:**
```bash
python3 -m venv venv
```

**On Windows:**
```bash
python -m venv venv
```

You should now see a `venv` folder in your project directory.

### 5. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Note:** If you get a PowerShell execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should now see `(venv)` at the beginning of your terminal prompt.

### 6. Select Python Interpreter in VS Code

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
2. Type: `Python: Select Interpreter`
3. Choose the interpreter from your `venv` folder
   - Should show something like `./venv/bin/python` or `.\venv\Scripts\python.exe`

### 7. Install Dependencies

With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - for API calls
- `pandas` - for data manipulation
- `openpyxl` - for Excel file creation

### 8. Configure Your League Settings

1. **Copy the example config:**
   ```bash
   cp examples/example_config.py config.py
   ```
   
   Or manually:
   - Copy `examples/example_config.py`
   - Paste it in the root directory
   - Rename to `config.py`

2. **Edit `config.py`:**
   
   Open `config.py` in VS Code and update:

   ```python
   # Your league ID (find it in your Sleeper URL)
   LEAGUE_IDS = ['1124822672346198016']  # Replace with yours
   
   # Current season
   START_YEAR = 2024
   
   # Where to save files - IMPORTANT: Update this path!
   BASE_OUTPUT_DIR = '/Users/yourname/Desktop/Fantasy'
   
   # Your league members
   NAME_MAP = {
       "sleeper_username1": "Real Name 1",
       "sleeper_username2": "Real Name 2",
       # ... add all your league members
   }
   ```

### 9. Run the Script

You have three options:

**Option 1: Run Button (Easiest)**
1. Open `main.py`
2. Click the ▶️ (play) button in the top-right corner
3. Watch the terminal for progress

**Option 2: Right-Click Menu**
1. Right-click in the `main.py` editor
2. Select "Run Python File in Terminal"

**Option 3: Terminal Command**
```bash
python main.py
```

### 10. View Your Data

After the script completes, check your `BASE_OUTPUT_DIR` for:
- `Annual_League_Data/` - League standings
- `Annual_Matchup_Data/` - Weekly matchups
- `Playoff_Data/` - Playoff results
- `Complete_Data/` - Combined file
- `*_HighLow_points_summary.xlsx` - Weekly highs/lows

## Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
- Make sure your virtual environment is activated (look for `(venv)` in terminal)
- Run: `pip install -r requirements.txt` again
- Verify you selected the correct Python interpreter in VS Code

### Issue: "config.py not found"
**Solution:**
- Make sure you copied `example_config.py` to `config.py`
- Check that it's in the root directory (same level as `main.py`)

### Issue: Terminal doesn't recognize `python` command
**Solution:**
- Try `python3` instead of `python`
- On Windows, you might need to use `py` instead of `python`

### Issue: Can't activate virtual environment (Windows PowerShell)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Failed to fetch data" errors
**Solution:**
- Check your internet connection
- Verify your league ID is correct
- Wait a minute and try again (might be rate-limited)

### Issue: Script is very slow
**Solution:**
- This is normal if `COLLECT_PLAYER_DATA = True`
- To speed up, edit `main.py` and set:
  ```python
  COLLECT_PLAYER_DATA = False
  ```

## VS Code Tips

### Debugging
1. Set breakpoints by clicking left of line numbers
2. Press `F5` to start debugging
3. Use Debug Console to inspect variables

### Terminal Shortcuts
- `` Ctrl+` `` - Toggle terminal
- `Cmd/Ctrl+Shift+5` - Split terminal
- `Cmd/Ctrl+C` - Stop running script

### File Navigation
- `Cmd/Ctrl+P` - Quick open file
- `Cmd/Ctrl+Shift+F` - Search across all files
- `Cmd/Ctrl+B` - Toggle sidebar

### Python-Specific
- `Shift+Enter` - Run selected code in Python Interactive
- `F12` - Go to definition
- `Shift+F12` - Find all references

## Customizing the Script

### Skip Certain Data Types

Edit flags in `main.py`:
```python
COLLECT_LEAGUE_DATA = True
COLLECT_MATCHUP_DATA = True
COLLECT_PLAYOFF_DATA = True
COLLECT_HIGHLOW_DATA = True
COLLECT_PLAYER_DATA = False  # Set to False to skip
```

### Change Output Format

Edit `SAVE_INDIVIDUAL_FILES` and `SAVE_COMBINED_FILE` in `main.py`.

### Adjust Scoring Settings

Edit `SCORING_SETTINGS` in your `config.py` to match your league's rules.

## Need Help?

1. Check the main [README.md](README.md) for general documentation
2. Review [Sleeper API docs](https://docs.sleeper.app/)
3. Open an issue on GitHub

## Next Steps

After running successfully once:
1. Add the output directory to your `.gitignore` so you don't commit data files
2. Update `config.py` each season with new league IDs
3. Consider scheduling to run automatically at season end

Happy coding! 🏈💻
