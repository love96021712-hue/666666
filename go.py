import streamlit as st
import json
import os

# --- 數據持久化 ---
DB_FILE = "settings.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"rate": 4.6396, "price_rmb": 8.1799}

def save_data(rate, price_rmb):
    with open(DB_FILE, "w") as f:
        json.dump({"rate": rate, "price_rmb": price_rmb}, f)

saved_data = load_data()

# --- 頁面配置 ---
st.set_page_config(page_title="天堂373計算機", layout="centered")

# --- 視覺強化 CSS ---
st.markdown("""
    <style>
    /* 調整整體頂部間距 */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    
    /* 標題框：增加高度與頂部內距，徹底解決切字 */
    .title-box {
        background-color: #1E1E1E;
        padding-top: 20px;    /* 增加上方間距，把字往下擠 */
        padding-bottom: 15px;
        padding-left: 15px;
        padding-right: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        border-left: 6px solid #FF4B4B;
        min-height: 70px;     /* 強制盒子高度 */
    }
    
    .main-title {
        font-size: 22px !important;
        color: white !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
        margin: 0 !important;
        display: block;
    }
    
    /* 大數字樣式 */
    [data-testid="stMetricValue"] {
        font-size: 42px !important;
        color: #FF4B4B;
        font-weight: bold;
    }
    
    /* 紅色利潤字體 */
    .p-red { 
        color: #FF4B4B; 
        font-weight: bold; 
        margin-left: 10px; 
    }
    
    .row-style { 
        padding: 8px 15px; 
        border-bottom: 1px solid #333; 
        font-size: 17px;
    }
    
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 標題顯示 ---
st.markdown('<div class="title-box"><span class="main-title">🎮 天堂373金幣套利計算機</span></div>', unsafe_allow_html=True)

# --- 輸入區 ---
rate = st.number_input("1. 匯率 (TWD/RMB)", value=float(saved_data["rate"]), format="%.4f", step=0.0001)
price_rmb = st.number_input("2. 每萬金 (RMB)", value=float(saved_data["price_rmb"]), format="%.4f", step=0.0001)

save_data(rate, price_rmb)

# 3. 每萬金台幣價
price_twd = rate * price_rmb
st.markdown(f"**3. 每萬金台幣價: ${price_twd:.4f}**")

# --- 核心性價比 ---
if price_twd > 0:
    gold_per_twd = 10000 / price_twd
else:
    gold_per_twd = 0.0

st.metric(label="4. 進貨性價比 (1元買到)", value=f"{gold_per_twd:,.2f} 金")

# --- 垂直利潤分析 ---
st.markdown("---")
st.markdown("**📈 賣出利潤對照**")

targets = [250, 240, 230, 220, 210]

for sell_price in targets:
    if sell_price > 0:
        profit_pct = ((gold_per_twd / sell_price) - 1) * 100
    else:
        profit_pct = 0
    
    st.markdown(f"""
        <div class="row-style">
            賣 {sell_price} 金 <span class="p-red">{profit_pct:+.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

st.caption("數據已自動存檔")