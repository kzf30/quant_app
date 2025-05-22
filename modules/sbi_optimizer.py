# sbi_optimizer.py
import streamlit as st
import pandas as pd
import numpy as np
import cvxpy as cp

def run():
    st.title("📈 SBIスクリーニングCSVからポートフォリオ最適化")

    uploaded_file = st.file_uploader("SBIスクリーニング結果CSVをアップロード", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("読み込んだデータ：", df.head())

        # 正しい列名に合わせて修正
        if "ROE(自己資本利益率)(%)" not in df.columns or "PBR(株価純資産倍率)(倍)" not in df.columns:
            st.error("このCSVには 'ROE(自己資本利益率)(%)' と 'PBR(株価純資産倍率)(倍)' の列が必要です。")
            return

        try:
            expected_returns = df["ROE(自己資本利益率)(%)"].fillna(0) / 100
            risks = df["PBR(株価純資産倍率)(倍)"].fillna(1)
            n = len(df)

            w = cp.Variable(n)
            objective = cp.Maximize(expected_returns @ w - 0.1 * cp.norm(risks @ w, 2))
            constraints = [cp.sum(w) == 1, w >= 0]
            prob = cp.Problem(objective, constraints)
            prob.solve()

            df["最適比率"] = np.round(w.value, 4)
            st.subheader("最適ポートフォリオ構成")
            st.dataframe(df[["銘柄名", "コード", "最適比率"]])
        except Exception as e:
            st.error(f"最適化中にエラーが発生しました: {e}")

