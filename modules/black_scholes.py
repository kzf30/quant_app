# black_scholes.py
import streamlit as st
import numpy as np
from scipy.stats import norm

def black_scholes_price(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price, d1, d2

def run():
    st.title("🧮 ブラック＝ショールズ オプション価格計算")

    S = st.number_input("現物価格 S", value=100.0)
    K = st.number_input("権利行使価格 K", value=100.0)
    T = st.number_input("満期までの期間 T (年)", value=1.0)
    r = st.number_input("無リスク金利 r", value=0.01)
    sigma = st.number_input("ボラティリティ σ", value=0.2)
    option_type = st.selectbox("オプションの種類", ["call", "put"])

    if st.button("価格計算"):
        price, d1, d2 = black_scholes_price(S, K, T, r, sigma, option_type)
        st.success(f"{option_type.capitalize()} オプション価格: {price:.2f}")
        st.markdown(f"**d1** = {d1:.4f}, **d2** = {d2:.4f}")
