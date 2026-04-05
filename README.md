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
