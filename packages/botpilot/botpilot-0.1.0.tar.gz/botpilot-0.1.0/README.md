readme = '''# BotPilot

**BotPilot** is a Python CLI tool for automating organizational tasks using Selenium, pandas, and Oracle connections. It can scaffold web bots and reconciliation bots with optional emailer, logging, and database support.

## 🚀 Installation

```bash
pip install botpilot


git clone https://github.com/your-org/botpilot.git
cd botpilot
pip install .

🛠 Usage
botpilot init web-bot 
botpilot init recon-bot 


Options
--with-db: Include database connection scaffolding

--emailer: Include emailer utility

Logging is enabled by default and stored in /logs.



📁 Generated Structure
MyBot/
├── main.py
├── downloads/
├── assets/
│   └── app.ini
├── logs/
├── reports/
└── shared/