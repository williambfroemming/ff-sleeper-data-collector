# Setup & GitHub Upload Checklist

## ✅ Before You Start

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] VS Code installed
- [ ] Git installed (if using GitHub)
- [ ] Your Sleeper League ID ready
- [ ] Location for output files decided

## ✅ Initial Setup (Do Once)

### 1. Get the Project
- [ ] Download or clone the `fantasy-football-sleeper` folder
- [ ] Place it somewhere accessible (e.g., Desktop or Documents)

### 2. Set Up Python Environment
- [ ] Open folder in VS Code
- [ ] Open integrated terminal (`` Ctrl+` ``)
- [ ] Create venv: `python3 -m venv venv`
- [ ] Activate venv:
  - Mac/Linux: `source venv/bin/activate`
  - Windows CMD: `venv\Scripts\activate`
  - Windows PowerShell: `venv\Scripts\Activate.ps1`
- [ ] See `(venv)` in terminal prompt
- [ ] Install dependencies: `pip install -r requirements.txt`

### 3. Configure for Your League
- [ ] Copy: `cp examples/example_config.py config.py`
- [ ] Edit `config.py`:
  - [ ] Add your `LEAGUE_IDS`
  - [ ] Set correct `START_YEAR`
  - [ ] Update `BASE_OUTPUT_DIR` path
  - [ ] Fill in `NAME_MAP` with all league members
  - [ ] Verify `SCORING_SETTINGS` match your league
- [ ] Save `config.py`

### 4. Test Run
- [ ] In VS Code, select Python interpreter (from venv)
- [ ] Open `main.py`
- [ ] Press F5 or run: `python main.py`
- [ ] Watch for errors
- [ ] Check output directory for Excel files
- [ ] Verify data looks correct

## ✅ GitHub Upload Checklist

### 1. Prepare Repository
- [ ] Go to [GitHub](https://github.com)
- [ ] Click "New repository"
- [ ] Name it: `fantasy-football-sleeper`
- [ ] Description: "Data collection tool for Sleeper fantasy football leagues"
- [ ] Choose Public or Private
- [ ] Don't initialize with README (we have one!)
- [ ] Click "Create repository"

### 2. Important: Update Personal Info
Before uploading, customize these files:

- [ ] **LICENSE** - Change `[Your Name]` to your actual name
- [ ] **README.md** - Update GitHub username in clone URL:
  ```
  git clone https://github.com/YOURUSERNAME/fantasy-football-sleeper.git
  ```
- [ ] **QUICKSTART.md** - Same URL update
- [ ] **VSCODE_SETUP.md** - Same URL update

### 3. Verify .gitignore
Confirm these are in `.gitignore`:
- [ ] `config.py` ✅ (keeps your league info private!)
- [ ] `venv/` ✅
- [ ] `*.xlsx` ✅
- [ ] `__pycache__/` ✅

### 4. Initial Commit & Push

In terminal (in project directory):

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Fantasy Football Data Collector"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOURUSERNAME/fantasy-football-sleeper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Checklist:
- [ ] `git init` completed
- [ ] `git add .` completed
- [ ] `git commit` completed with message
- [ ] `git remote add` completed (with YOUR username)
- [ ] `git push` completed successfully
- [ ] Go to your GitHub repo URL and verify files are there

### 5. Verify GitHub Upload
Visit your repository and check:
- [ ] All Python files visible
- [ ] README.md displays correctly
- [ ] `config.py` is NOT there (good!)
- [ ] `venv/` folder is NOT there (good!)
- [ ] No `.xlsx` files (good!)
- [ ] `examples/example_config.py` IS there (good!)

### 6. Make It Professional
Add these to your GitHub repo:

- [ ] Add topics/tags: `python`, `fantasy-football`, `sleeper`, `data-collection`
- [ ] Add description
- [ ] Consider adding a screenshot to README
- [ ] Add a release/version tag (optional)

## ✅ Annual Usage Checklist

When new season starts:

- [ ] Update `config.py` with new:
  - [ ] `LEAGUE_IDS` (if league ID changed)
  - [ ] `START_YEAR`
  - [ ] `NAME_MAP` (if members changed)
- [ ] Pull latest code: `git pull`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Run: `python main.py`
- [ ] Verify Excel files created
- [ ] Import to your database

## ✅ Sharing With Others

If you want others to use this:

- [ ] Make sure `config.py` is in `.gitignore` ✅
- [ ] Ensure `example_config.py` is complete and documented
- [ ] Update README with any special instructions
- [ ] Test installation on a fresh clone
- [ ] Add issues/discussions section on GitHub
- [ ] Consider adding screenshots or example output

## ✅ Maintenance Checklist

Periodically:

- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Test with new Sleeper API changes
- [ ] Update documentation if you add features
- [ ] Commit and push changes: `git add .` → `git commit -m "message"` → `git push`

## 📝 Quick Reference

### Common Git Commands
```bash
git status              # Check what's changed
git add .               # Stage all changes
git commit -m "msg"     # Commit with message
git push                # Push to GitHub
git pull                # Get latest from GitHub
```

### Common Python Commands
```bash
source venv/bin/activate    # Activate venv (Mac/Linux)
venv\Scripts\activate       # Activate venv (Windows)
deactivate                  # Deactivate venv
pip list                    # See installed packages
python main.py              # Run the script
```

### VS Code Shortcuts
- `` Ctrl+` `` - Toggle terminal
- `F5` - Run/Debug
- `Cmd/Ctrl+P` - Quick open file
- `Cmd/Ctrl+Shift+P` - Command palette

## 🎉 You're Done!

Once all boxes are checked:
- ✅ Your project is properly structured
- ✅ It's on GitHub for version control
- ✅ Others can clone and use it
- ✅ You can update it easily

## 📞 Need Help?

- Check [README.md](README.md) for documentation
- See [VSCODE_SETUP.md](VSCODE_SETUP.md) for VS Code help
- See [QUICKSTART.md](QUICKSTART.md) for quick setup
- Open an issue on GitHub

---

**Pro Tip:** After your first successful run, create a git commit:
```bash
git add .
git commit -m "Successfully collected data for [SEASON YEAR]"
git push
```

This creates a historical record of when you collected each season's data!
