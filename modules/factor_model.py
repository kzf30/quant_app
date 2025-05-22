# factor_model.py
import streamlit as st
import pandas as pd
import statsmodels.api as sm

def run():
    st.title("📐 ファクターモデルによるリターン要因分析")

    st.markdown("ファクター（例：市場リターン、サイズ、バリュー）と株式リターンの関係を回帰分析で評価します。")

    returns_file = st.file_uploader("株式リターンCSV（Date, Return列）", type="csv", key="ret")
    factors_file = st.file_uploader("ファクターCSV（Date列と要因列）", type="csv", key="fac")

    if returns_file and factors_file:
        try:
            returns_df = pd.read_csv(returns_file)
            factors_df = pd.read_csv(factors_file)

            merged = pd.merge(returns_df, factors_df, on="Date")
            y = merged["Return"]
            X = merged.drop(columns=["Date", "Return"])
            X = sm.add_constant(X)

            model = sm.OLS(y, X).fit()
            st.subheader("回帰結果")
            st.text(model.summary())
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
