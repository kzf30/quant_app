# news_analysis.py
import streamlit as st
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def run():
    st.title("📰 経済ニュースからキーワード抽出")

    rss_url = st.text_input("RSSフィードURLを入力", value="https://www.nikkei.com/rss/markets.xml")

    if st.button("ニュース解析"):
        feed = feedparser.parse(rss_url)
        titles = [entry.title for entry in feed.entries]
        all_text = " ".join(titles)

        st.write("取得した見出し数：", len(titles))
        st.write("例：", titles[:5])

        wordcloud = WordCloud(width=800, height=400, background_color="white", font_path=None).generate(all_text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
