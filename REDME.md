AI_Trading_System_ki
A modular, self-learning AI trading system for cryptocurrency and forex markets, featuring a responsive dashboard, smart VPN integration, and advanced NLP-based sentiment analysis. Built for Windows and VPS environments with a focus on scalability, security, and performance.
Owned by Khaleq Salehi. Any use of this project or contributions to its development require explicit permission from Khaleq Salehi. Developed with code contributions and consultation from Qwen.
Table of Contents

Project Overview
Features
Roadmap
Folder Structure
Installation
Usage
Dependencies
Contributing
Acknowledgments
License
Contact

Project Overview
AI_Trading_System_ki is an advanced trading platform solely owned by Khaleq Salehi. It leverages reinforcement learning (RL), natural language processing (NLP), and real-time market data to execute optimized trading strategies. The system features a modular architecture, ensuring plug-and-play components, robust security, and compatibility with Windows and VPS environments. It includes a responsive Dash-based dashboard, smart VPN switching, and an external REST API for remote control. Qwen has contributed to code development and provided architectural guidance.
Features

Modular Architecture: Clean folder structure with dedicated modules for strategies, UI, APIs, logs, models, and utilities.
Self-Learning AI: Reinforcement learning for adaptive strategy optimization, supported by backtesting (backtester.py) and market replay (market_replay.py).
Exchange API Integration: Smart failover for reliable connections to crypto and forex exchanges, configurable via UI.
Responsive Dashboard: Built with Dash, featuring real-time logs, stats, strategy settings, market data, and VPN status.
Sentiment Analysis: NLP-driven news and sentiment analysis using HuggingFace models, NLTK, and VADER.
Smart VPN Module: Automatic server switching for V2Ray/VPN connections, with status displayed in the UI.
Security: Encrypted API keys and optimized performance for low-latency trading.
External API: REST endpoints (e.g., /pause, /status, /retrain) for remote system control.

Roadmap

Phase 1 (Q3 2025): Implement basic backtesting, one trading strategy, and exchange API integration.
Phase 2 (Q4 2025): Develop Dash dashboard and lightweight NLP sentiment analysis.
Phase 3 (Q1 2026): Integrate RL for strategy optimization and smart VPN module.
Phase 4 (Q2 2026): Add external REST API and optimize for production-scale performance.

Folder Structure
D:\AI\AI_Trading_System_v7
├── /strategies        # Trading strategies and logic
├── /ui                # Dash-based dashboard components
├── /api               # Exchange API connectors and external REST API
├── /logs              # System logs and error tracking
├── /models            # RL and NLP models
├── /utils             # Helper functions and utilities
├── app.py             # Main application entry point
├── backtester.py      # Backtesting module
├── config.yaml        # Configuration settings
├── dashboard_main.py  # Dashboard initialization
├── market_replay.py   # Market replay for testing
├── requirements.txt   # Python dependencies

Installation
Prerequisites

Python 3.11
Windows or VPS environment
Offline Python packages in E:\Programing\pyton\pack (or download from non-sanctioned sources like https://pypi.tuna.tsinghua.edu.cn/simple)

Steps

Clone the Repository (requires permission from Khaleq Salehi):git clone https://github.com/khalegh2131/AI_Trading_System_ki.git
cd AI_Trading_System_ki


Set Up Virtual Environment:python -m venv venv
.\venv\Scripts\activate


Install Dependencies:
If using offline packages:pip install --no-index --find-links=E:\Programing\pyton\pack -r requirements.txt


If online, use non-sanctioned mirrors.


Configure Settings:
Edit config.yaml to set API keys, exchange pairs, and VPN subscription links.


Run the Application (only with explicit permission):python app.py



Usage

Launch the dashboard: python dashboard_main.py
Configure trading strategies and API connections via the UI.
Run backtests using backtester.py or simulate with market_replay.py.
Monitor real-time logs, stats, and VPN status in the dashboard.
Control the system remotely via REST API (e.g., POST /pause).

Note: Usage of this system in any form requires explicit permission from Khaleq Salehi.
Dependencies
Key dependencies (see requirements.txt for full list):

dash: Responsive dashboard
pandas: Data manipulation
numpy: Numerical operations
requests: API connections
huggingface_hub: NLP models
nltk: Sentiment analysis
vaderSentiment: Sentiment scoring
pyyaml: Configuration parsing
pytest: Unit testing

Contributing
This project is owned by Khaleq Salehi, and all contributions or use of the codebase require his explicit permission. If you’re passionate about AI, trading, or software development, we’d love your help to make this project a reality! Here’s how you can contribute:

Contact Khaleq Salehi via email (khaleq.sa@gmail.com) or GitHub Issues to discuss your proposed contribution.
Fork the repository (only after approval).
Create a feature branch (git checkout -b feature/new-feature).
Commit changes (git commit -m "Add new feature").
Push to the branch (git push origin feature/new-feature).
Open a pull request with a clear description, referencing your prior approval.

What we need help with:

Coding trading strategies or RL models
Designing the dashboard UI/UX
Optimizing performance for VPS
Testing and debugging APIs or VPN integration

Important: Unauthorized use or modification of this project is strictly prohibited.
Acknowledgments

Khaleq Salehi: Project owner, lead developer, and visionary.
Qwen: Assisted with code generation and implementation of key features.
Community: We invite approved contributors to join and help build this exciting project!

License
This project is proprietary and owned by Khaleq Salehi. Usage, modification, or distribution requires explicit permission from Khaleq Salehi. See LICENSE file for details.
Contact Details
For questions, collaboration requests, or permission to use or contribute, contact:Khaleq Salehi📧 Email: khaleq.sa@gmail.com🌐 GitHub: github.com/khalegh2131
## Project Structure
- `app.py`: Main application entry point
- `api/main_api.py`: Core API functionality
- `core/`: Backtesting and strategy optimization modules
- `strategies/`: Trading strategy implementations
- `ui/dashboard_main.py`: User interface for the trading system
- `scripts/`: Utility scripts (e.g., data downloading)

## Installation
1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py` or `python api/main_api.py`

## Usage
- Run `app.py` for the main application.
- Use `api/main_api.py` for API interactions.
- Run `scripts/download_klines.py` to fetch market data.
