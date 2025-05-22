import streamlit as st

st.set_page_config(layout="wide")
st.title("💼 クオンツ×金融工学 統合ダッシュボード")

modules = {
    "SBIポートフォリオ最適化": "sbi_optimizer",
    "ブラック＝ショールズ理論価格": "black_scholes",
    "モンテカルロ・シミュレーション": "monte_carlo",
    "ファクターモデル分析": "factor_model",
    "インプライド・ボラティリティ推定": "implied_vol",
    "ニューストピック分析": "news_analysis",
}

choice = st.sidebar.selectbox("分析モジュールを選択", list(modules.keys()))

module = __import__(f"modules.{modules[choice]}", fromlist=["run"])
module.run()
