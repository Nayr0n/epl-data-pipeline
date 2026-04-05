# ⚽ Premier League ETL Pipeline & Dashboard

An end-to-end data pipeline that extracts live English Premier League match data, enriches it with local metadata, and visualizes the current standings via an interactive web dashboard.

## 🚀 Overview

This project demonstrates a complete Data Engineering workflow (Extract, Transform, Load) and Presentation layer. It automates the process of fetching raw match results, calculating league standings (points, goal difference, form), and presenting them in a user-friendly UI. 

Crucially, it handles **data enrichment** by merging dynamic REST API data with a local static JSON dataset.

## ✨ Key Features

- **Automated ETL Process:** Fetches data, calculates W-D-L stats, goals, and tie-breakers based on official EPL rules.
- **Multiple Data Sources:** Integrates live match data from `football-data.org` API with static team metadata (stadiums, founding years) from a local `teams_info.json` file.
- **Robust Error Handling:** Implements `.get()` fallbacks and `try-except` blocks to handle missing metadata files or API rate limits gracefully without crashing the pipeline.
- **Persistent Storage:** Uses a lightweight `SQLite` database to store processed data, minimizing external API calls.
- **Interactive UI:** A custom `Streamlit` dashboard featuring a clean standings table with team crests and an interactive section for team metadata.

## 🛠️ Tech Stack

- **Language:** Python 3
- **Data Extraction & Transformation:** `requests`, `pandas`, `json`
- **Database:** `SQLite3`
- **Frontend / Visualization:** `Streamlit`

## 📁 Project Structure

```text
├── script.py           # The main ETL script (Extract, Transform, Load)
├── app.py              # Streamlit web dashboard (Presentation Layer)
├── teams_info.json     # Local static metadata source
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## ⚙️ Setup and Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/Nayr0n/epl-data-pipeline.git](https://github.com/Nayr0n/epl-data-pipeline.git)
cd epl-data-pipeline
```

**2. Install required dependencies:**
```bash
pip install -r requirements.txt
```

**3. API Key Configuration:**
- Get a free API key from [football-data.org](https://www.football-data.org/).
- Open `script.py` and replace `YOUR_API_KEY_HERE` with your actual key.

## 🏃‍♂️ How to Run

**Step 1: Run the ETL Pipeline**
Execute the script to fetch latest data, process it, and update the database:
```bash
python script.py
```
*(You should see success messages in the terminal confirming data extraction, transformation, and database loading).*

**Step 2: Launch the Dashboard**
Start the Streamlit web application:
```bash
python -m streamlit run app.py
```
The dashboard will open automatically in your default web browser (usually at `http://localhost:8501`).

## 📈 Future Improvements
- Containerize the application using **Docker**.
- Implement a task scheduler (e.g., **Cron** or **Apache Airflow**) to automate the ETL script execution after match days.
- Add real-time top scorer and injury statistics via additional APIs.
