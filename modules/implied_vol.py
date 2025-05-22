# implied_vol.py
import streamlit as st
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def bs_price(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def implied_vol(S, K, T, r, market_price, option_type):
    try:
        return brentq(lambda sigma: bs_price(S, K, T, r, sigma, option_type) - market_price, 1e-6, 5)
    except ValueError:
        return None

def run():
    st.title("📈 インプライド・ボラティリティ（IV）推定")

    S = st.number_input("現物価格 S", value=100.0)
    K = st.number_input("権利行使価格 K", value=100.0)
    T = st.number_input("残存期間 T（年）", value=1.0)
    r = st.number_input("無リスク金利 r", value=0.01)
    market_price = st.number_input("市場オプション価格", value=10.0)
    option_type = st.selectbox("オプションの種類", ["call", "put"])

    if st.button("インプライド・ボラを計算"):
        iv = implied_vol(S, K, T, r, market_price, option_type)
        if iv:
            st.success(f"インプライド・ボラティリティ: {iv:.4f}")
        else:
            st.error("計算できませんでした（価格が理論値の範囲外の可能性があります）")
