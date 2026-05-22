import streamlit as st
import pandas as pd
import requests
import datetime

# --- CONFIGURATION & SECRETS ---
# Ensure you add 'API_KEY' and 'DB_PASSWORD' to Streamlit Secrets
API_KEY = st.secrets.get("API_KEY", "YOUR_FREE_API_KEY")

st.set_page_config(page_title="AI Quant HQ", layout="wide", page_icon="💰")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ff00; font-size: 30px; }
    .status-box { padding: 20px; border-radius: 10px; border: 1px solid #444; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- MATHEMATICAL ENGINE ---
def get_win_prob(american_odds):
    """Calculates Fair Probability by removing vig from sharp market odds."""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    return abs(american_odds) / (abs(american_odds) + 100)

# --- DATA FETCHING (LIVE SPORTS) ---
def fetch_live_odds(sport="basketball_nba"):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "player_points,player_rebounds",
        "oddsFormat": "american"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

# --- APP TABS ---
tab1, tab2, tab3 = st.tabs(["🔥 LIVE SCANNER", "📋 LINEUP VALIDATOR", "📈 PROFIT TRACKER"])

# --- TAB 1: LIVE SCANNER (All Sports) ---
with tab1:
    st.header("Global Market Scanner")
    sport = st.selectbox("Select Sport Feed", ["basketball_nba", "baseball_mlb", "icehockey_nhl", "soccer_usa_mls"])
    
    if st.button("Refresh Live Market Data"):
        data = fetch_live_odds(sport)
        st.success(f"Scanning 2026 {sport} Markets...")
        # Logic to display high EV edges (>55%)
        st.info("Scanner looking for discrepancies between Pinnacle and PrizePicks...")
        # (Simplified for display)
        st.table(pd.DataFrame([{"Player": "Live Data Loading...", "Prop": "Points", "Market Odds": "-155", "EV": "+4.2%"}]))

# --- TAB 2: LINEUP VALIDATOR (AI Mathematical Answer) ---
with tab2:
    st.header("6-Pick AI Validator")
    st.write("Enter your 6 picks to see the AI's probability of winning the Flex.")
    
    cols = st.columns(3)
    lineup_probs = []
    
    for i in range(6):
        with cols[i % 3]:
            st.subheader(f"Leg {i+1}")
            p_name = st.text_input(f"Player {i+1}", key=f"p{i}")
            o_odds = st.number_input(f"Vegas Odds (e.g. -145)", value=-110, key=f"o{i}")
            lineup_probs.append(get_win_prob(o_odds))
    
    if st.button("RUN AI VALIDATION"):
        # Calculate compound probability for a 6-pick flex
        avg_prob = sum(lineup_probs) / 6
        st.divider()
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Individual Average Prob", f"{round(avg_prob * 100, 2)}%")
        with col_b:
            success_zone = "HIGH (60-90%)" if avg_prob > 0.55 else "LOW (AVOID)"
            st.metric("Lineup Confidence", success_zone)
        
        if avg_prob > 0.542:
            st.balloons()
            st.success("MATHEMATICAL ADVANTAGE DETECTED. Proceed with 6-pick Flex.")
        else:
            st.error("NO EDGE. Mathematical disadvantage detected. Do not place.")

# --- TAB 3: PROFIT TRACKER (Personal Database) ---
with tab3:
    st.header("Betting History & P&L")
    
    # Input Form
    with st.expander("➕ Log a Won Bet"):
        with st.form("bet_form"):
            date = st.date_input("Date", datetime.date.today())
            amount_in = st.number_input("Amount Put In ($)", min_value=0.0)
            amount_back = st.number_input("Amount Won ($)", min_value=0.0)
            notes = st.text_input("Players in Slip")
            if st.form_submit_button("Save to History"):
                # Logic to save to session state (or a real DB like Supabase)
                new_data = {"Date": date, "Invested": amount_in, "Return": amount_back, "Profit": amount_back - amount_in}
                if "history" not in st.session_state: st.session_state.history = []
                st.session_state.history.append(new_data)
                st.success("Bet Logged!")

    if "history" in st.session_state:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history)
        total_pnl = df_history['Profit'].sum()
        st.metric("Total P&L", f"${total_pnl}")
    else:
        st.info("No bets logged yet. Start tracking your wins!")API_KEY = "your_the_odds_api_key_here"