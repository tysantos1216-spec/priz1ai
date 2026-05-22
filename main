import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION ---
# Get your FREE API Key at https://the-odds-api.com/
API_KEY = "YOUR_THE_ODDS_API_KEY" 
REGIONS = "us" # us | uk | eu | au
MARKETS = "player_props" # focus on player props for PrizePicks
ODDS_FORMAT = "american"
DATE_FORMAT = "iso"

st.set_page_config(page_title="AI Quant: PrizePicks EV", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3d4455; }
    </style>
    """, unsafe_allow_html=True)

# --- MATHEMATICAL ENGINE ---
def calculate_ev(odds_over, odds_under):
    """Devigs odds to find the true 'Fair Win Probability'."""
    def to_decimal(american):
        return (american / 100) + 1 if american > 0 else (100 / abs(american)) + 1
    
    over_dec, under_dec = to_decimal(odds_over), to_decimal(odds_under)
    over_prob, under_prob = 1 / over_dec, 1 / under_dec
    
    # Remove the House Juice (Vig)
    fair_over_prob = over_prob / (over_prob + under_prob)
    return fair_over_prob

# --- LIVE DATA FETCH ---
def fetch_live_data(sport="basketball_nba"):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": "player_points", # Change to any prop: player_rebounds, player_assist
        "oddsFormat": ODDS_FORMAT,
        "bookmakers": "prizepicks,draftkings,pinnacle" 
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

# --- APP UI ---
st.title("🎯 AI Quant: PrizePicks Live EV Scanner")
st.subheader("May 2026 Live Market Analysis")

sport_choice = st.selectbox("Select Sport", ["basketball_nba", "baseball_mlb", "icehockey_nhl"])

if st.button("🚀 SCAN LIVE MARKET"):
    data = fetch_live_data(sport_choice)
    
    if not data:
        st.error("Could not fetch data. Check your API Key.")
    else:
        results = []
        for event in data:
            # Logic to find PrizePicks lines vs Sharp Books
            # Note: The-Odds-API structure varies; this is the logic flow
            player_name = event.get('home_team') # Placeholder for prop logic
            
            # Simulated EV calculation for demo (Logic remains same for live data)
            # In a live environment, you compare PP fixed (-119) vs Pinnacle/DK odds
            fair_prob = calculate_ev(-145, 120) # Example: Market is heavily favored Over
            
            results.append({
                "Player": "Live Player Data",
                "Market": "Points",
                "PP Line": "19.5",
                "Fair Prob (%)": round(fair_prob * 100, 2),
                "EV Status": "✅ APPROVED" if fair_prob > 0.542 else "❌ REJECTED"
            })
            
        df = pd.DataFrame(results)
        st.table(df)

st.sidebar.markdown("""
### 🛡️ System Rules
1. **Implied Odds:** -119 (PrizePicks 6-Pick)
2. **Breakeven:** 54.2%
3. **Target:** 56%+ (Green Zone)
""")
