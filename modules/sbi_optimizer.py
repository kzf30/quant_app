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

        roe_col = "ROE(自己資本利益率)(%)"
        pbr_col = "PBR(株価純資産倍率)(倍)"

        if roe_col not in df.columns or pbr_col not in df.columns:
            st.error(f"このCSVには '{roe_col}' と '{pbr_col}' の列が必要です。")
            return

        try:
            expected_returns = df[roe_col].fillna(0) / 100
            risks = df[pbr_col].fillna(1)
            n = len(df)

            w = cp.Variable(n)
            objective = cp.Maximize(expected_returns @ w - 0.1 * cp.norm(risks @ w, 2))
            constraints = [cp.sum(w) == 1, w >= 0]
            prob = cp.Problem(objective, constraints)
            prob.solve()

            df["最適比率"] = np.round(w.value, 4)
            st.subheader("✅ 最適ポートフォリオ構成")
            st.dataframe(df[["銘柄名", "コード", "最適比率"]])
        except Exception as e:
            st.error(f"最適化中にエラーが発生しました: {e}")

