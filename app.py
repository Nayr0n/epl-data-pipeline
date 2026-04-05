import streamlit as st
import sqlite3
import pandas as pd

# This Streamlit application serves as the Presentation Layer for the Premier League Data Pipeline.
#
# It reads processed and enriched data from a local SQLite database ('premier_league.db'). 
# The dashboard displays the current league standings using custom HTML/CSS for team crests
# and includes an interactive section showcasing team metadata (Stadium and Founding Year), 
# which was merged from a secondary local JSON source during the ETL process.
#
# Prerequisites:
# - Ensure 'streamlit' and 'pandas' are installed (`pip install streamlit pandas`).
# - Run the ETL pipeline (`python script.py`) FIRST to generate and populate the database.
#
# Usage:
# - Launch the dashboard using: `python -m streamlit run app.py`

st.set_page_config(page_title="EPL Standings Dashboard", layout="wide")

st.title("🏆 Premier League Standings")

def get_data():
    conn = sqlite3.connect('premier_league.db')
    query = "SELECT crest_url, team_name, played, wins, draws, losses, goals_for, goals_against, gd, points, form, stadium, founded FROM standings ORDER BY points DESC, gd DESC, goals_for DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = get_data()

if not df.empty:
    df['Team'] = df.apply(lambda x: f"<img src='{x['crest_url']}' width='25' style='vertical-align: middle; margin-right: 10px;'> {x['team_name']}", axis=1)
    df.insert(0, 'Pos', range(1, len(df) + 1))
    
    display_df = df[['Pos', 'Team', 'played', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'gd', 'points', 'form']]
    display_df.columns = ['Pos', 'Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'Form']

    st.write(
        display_df.to_html(escape=False, index=False, justify='center'), 
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
            table { width: 100%; border-collapse: collapse; color: white; font-family: sans-serif; }
            th { background-color: #1f2a3d; text-align: center !important; padding: 12px; }
            td { text-align: center; padding: 10px; border-bottom: 1px solid #444; }
            
            td:nth-child(2), th:nth-child(2) { 
                text-align: left !important; 
                padding-left: 20px; 
            }
            
            tr:hover { background-color: #262730; }
        </style>
    """, unsafe_allow_html=True)
    
    st.write("Data fetched from football-data.org and processed via custom ETL pipeline.")

    st.divider()
    st.subheader("📝 League Rules")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**Points:** Win: 3 pts | Draw: 1 pt | Loss: 0 pts")
    with c2:
        st.info("**Tie-breakers:** 1. Points | 2. Goal Difference | 3. Goals Scored")

    st.divider()
    st.subheader("🏟️ Team Information")
    
    selected_team = st.selectbox("Select a team to view details:", df['team_name'].tolist())
    
    team_data = df[df['team_name'] == selected_team].iloc[0]
    
    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="Stadium", value=team_data.get('stadium', 'N/A'))
    with col4:
        st.metric(label="Year Founded", value=team_data.get('founded', 'N/A'))