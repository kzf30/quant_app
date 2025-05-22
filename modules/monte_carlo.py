# monte_carlo.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📊 モンテカルロ法による株価シミュレーション")

    S0 = st.number_input("初期株価 S₀", value=100.0)
    mu = st.number_input("期待リターン μ", value=0.05)
    sigma = st.number_input("ボラティリティ σ", value=0.2)
    T = st.number_input("期間 T（年）", value=1.0)
    n_simulations = st.slider("シミュレーション数", 100, 5000, 1000)
    n_steps = st.slider("ステップ数", 50, 500, 100)

    if st.button("実行"):
        dt = T / n_steps
        prices = np.zeros((n_steps + 1, n_simulations))
        prices[0] = S0

        for t in range(1, n_steps + 1):
            z = np.random.standard_normal(n_simulations)
            prices[t] = prices[t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(prices)
        ax.set_title("モンテカルロシミュレーションによる株価パス")
        ax.set_xlabel("時間ステップ")
        ax.set_ylabel("株価")
        st.pyplot(fig)
