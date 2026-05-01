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

# --- 視覺強化 CSS (緊湊版) ---
st.markdown("""
    <style>
    /* 全局間距縮減 */
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    div[data-testid="stVerticalBlock"] > div { padding-top: 0rem; padding-bottom: 0.1rem; }
    
    .title-box {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        border-left: 6px solid #FF4B4B;
    }
    
    .main-title {
        font-size: 22px !important;
        color: white !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }
    
    /* 大數字樣式 */
    [data-testid="stMetricValue"] {
        font-size: 42px !important;
        color: #FF4B4B;
        font-weight: bold;
        line-height: 1 !important;
    }
    
    /* 調整 307.91 下方的間距 */
    [data-testid="stMetric"] { margin-bottom: -15px; }

    .p-red { 
        color: #FF4B4B; 
        font-weight: bold; 
        margin-left: 10px; 
    }
    
    /* 列表行：縮小內距 */
    .row-style { 
        padding: 4px 15px; 
        border-bottom: 1px solid #333; 
        font-size: 16px;
    }
    
    /* 移除所有 P 標籤的預設間距 */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 標題顯示 ---
st.markdown('<div class="title-box"><span class="main-title">🎮 天堂373金幣套利計算機</span></div>', unsafe_allow_html=True)

# --- 輸入區 ---
rate = st.number_input("1. 匯率 (TWD/RMB)", value=float(saved_data["rate"]), format="%.4f", step=0.0001)
price_rmb = st.number_input("2. 每萬金 (RMB)", value=float(saved_data["price_rmb"]), format="%.4f", step=0.0001)

save_data(rate, price_rmb)

# 計算台幣價
price_twd = rate * price_rmb
st.markdown(f"**3. 每萬金台幣價: ${price_twd:.4f}**")

# --- 核心性價比 ---
if price_twd > 0:
    gold_per_twd = 10000 / price_twd
else:
    gold_per_twd = 0.0

# 顯示性價比 (移除標籤間距)
st.metric(label="4. 進貨性價比 (1元買到)", value=f"{gold_per_twd:,.2f} 金")

# --- 動態利潤分析 (直接緊跟在後) ---
st.markdown("<br>**📈 動態賣出利潤對照**", unsafe_allow_html=True)

# 邏輯：基準點往下跳 5, 10, 15, 20
base_price = int(gold_per_twd // 5) * 5
dynamic_targets = [base_price - (i * 5) for i in range(0, 4)]

for sell_price in dynamic_targets:
    if sell_price > 0:
        profit_pct = ((gold_per_twd / sell_price) - 1) * 100
        st.markdown(f'<div class="row-style">賣 {sell_price} 金 <span class="p-red">{profit_pct:+.1f}%</span></div>', unsafe_allow_html=True)

st.markdown(f'<p style="color: grey; font-size: 12px; margin-top: 10px;">數據已自動存檔</p>', unsafe_allow_html=True)