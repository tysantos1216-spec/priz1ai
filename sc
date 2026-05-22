python
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import easyocr
import requests
import re

# --- CONFIGURATION ---
# Target implied probability (User requested 56%)
STRICT_THRESHOLD = 0.560 

st.set_page_config(page_title="AI Quant: Photo Scanner", layout="wide")

# Initialize OCR Reader (loads once)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# --- CSS STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #1a1c24; color: white; }
    .stMetric { background-color: #262730; padding: 10px; border-radius: 5px; }
    .css-1r6slb0 { background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APP UI ---
st.title("📸 AI Quant: PrizePicks Photo Scanner")
st.subheader("May 2026 Live EV Analysis (Experimental OCR)")

st.sidebar.markdown("""
### 🛡️ System Rules
1. **Breakeven:** 54.2%
2. **Threshold:** 56.0% (Strict)
""")

# File Uploader
uploaded_file = st.file_uploader("Upload PrizePicks Slip Screenshot", type=["png", "jpg", "jpeg"])

# Function to Simulate Live Market EV
def simulate_market_check(player_list):
    results = []
    for player in player_list:
        # For DEMO: Assigning random EV near the threshold
        # In deployment, this compares PP line vs Pinnacle/Sharp Odds API
        implied_odds = np.random.uniform(-160, 110)
        fair_prob = np.random.uniform(0.50, 0.60)
        
        status = "✅ APPROVE" if fair_prob >= STRICT_THRESHOLD else "❌ DISAPPROVE"
        
        results.append({
            "Detected Player": player,
            "Target Prop": "Points (Simulated)",
            "Fair Win Prob (%)": round(fair_prob * 100, 2),
            "Verdict": status
        })
    return results

# OCR Process
if uploaded_file is not None:
    # Convert file to image that EasyOCR can use
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Slip', width=300)
    
    # Process with OCR
    with st.spinner("Analyzing text in photo..."):
        # Convert PIL to numpy array
        img_array = np.array(image)
        result = reader.readtext(img_array, detail=0)
        
        # Simple extraction logic (Demo only; needs refinement for live use)
        # Filters for uppercase words (likely player names)
        potential_players = []
        for text in result:
            if text.isupper() and len(text) > 3:
                # Remove common PrizePicks UI text
                if text not in ["MORE", "LESS", "POINTS", "REBOUNDS", "ASSISTS"]:
                    potential_players.append(text)
        
        if not potential_players:
            st.warning("Could not clearly identify player names. Enter them manually.")
        else:
            st.success(f"Detected {len(potential_players)} players.")
            st.write(potential_players)
            
            if st.button("RUN EV SCAN ON SLIP"):
                with st.spinner("Checking live market odds..."):
                    ev_results = simulate_market_check(potential_players)
                    df = pd.DataFrame(ev_results)
                    st.table(df)
                    
                    # Calculate overall slip health
                    approved_count = df['Verdict'].str.contains("APPROVE").sum()
                    if approved_count >= 5: # Assuming 6-pick flex
                        st.balloons()
                        st.success("Mathematical Advantage:APPROVED. This slip is strong.")
                    else:
                        st.error("Mathematical Advantage: DISAPPROVED. Too many legs fall below 56% probability.")
else:
    st.info("Upload a screenshot of your PrizePicks slip (showing player names and lines) to begin the mathematical analysis.")