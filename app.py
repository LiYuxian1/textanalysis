import streamlit as st
import re
import jieba
from collections import Counter
from bs4 import BeautifulSoup
import requests
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import streamlit.components.v1 as components
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
from pyecharts.charts import Boxplot
from pyecharts.charts import Radar


# 抓取网页文本内容
def crawl_text(url):
    try:
        response = requests.get(url)
        #response.encoding = 'utf - 8'
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.find('body')
        if body_content:
            for script in body_content.find_all('script'):
                script.extract()
            for style in body_content.find_all('style'):
                style.extract()
            text_content = body_content.get_text(strip=True)
            return text_content
    except Exception as e:
        st.error(f"抓取网页内容出错: {e}")
        return None


# 对文本分词并统计词频
def process_text(text):
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    words = jieba.lcut(text)
    word_counts = Counter(words)
    return word_counts


# 绘制词云
def draw_wordcloud(word_counts):
    wordcloud = WordCloud()
    data = [(word, count) for word, count in word_counts.items()]
    wordcloud.add("", data, word_size_range=[20, 100])
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云"))
    return wordcloud


# 绘制条形图
def draw_bar_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    bar = (
        Bar()
        .add_xaxis(words)
        .add_yaxis("词频", counts)
        .set_global_opts(title_opts=opts.TitleOpts(title="词频条形图"))
    )
    return bar


# 绘制其他6种图形（这里简单示例折线图、饼图、散点图、箱线图、雷达图）
def draw_line_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    line = (
        Line()  # 这里使用Line类
        .add_xaxis(words)
        .add_yaxis("词频", counts)
        .set_global_opts(title_opts=opts.TitleOpts(title="词频折线图"))
    )
    return line


def draw_pie_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    pie = (
        Pie()
        .add("", list(zip(words, counts)))
        .set_global_opts(title_opts=opts.TitleOpts(title="词频饼图"))
    )
    return pie


def draw_scatter_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    scatter = (
        Scatter()
        .add_xaxis(words)
        .add_yaxis("词频", counts)
        .set_global_opts(title_opts=opts.TitleOpts(title="词频散点图"))
    )
    return scatter


def draw_boxplot_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    boxplot = (
        Boxplot()
        .add_xaxis(["词频"])
        .add_yaxis("", [counts])
        .set_global_opts(title_opts=opts.TitleOpts(title="词频箱线图"))
    )
    return boxplot


def draw_radar_chart(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    words, counts = zip(*sorted_words)
    radar_schema = [{"name": word, "max": max(counts)} for word in words]
    radar = (
        Radar()
        .add_schema(schema=radar_schema)
        .add("", [counts])
        .set_global_opts(title_opts=opts.TitleOpts(title="词频雷达图"))
    )
    return radar


# Streamlit应用
def main():
    st.sidebar.title("图形选择")
    chart_type = st.sidebar.selectbox(
        "选择图形类型",
        ["词云", "条形图", "折线图", "饼图", "散点图", "箱线图", "雷达图"]
    )

    st.title("文章词频分析")
    url = st.text_input("请输入文章URL:")
    if url:
        text = crawl_text(url)
        if text:
            word_counts = process_text(text)
            if chart_type == "词云":
                wordcloud = draw_wordcloud(word_counts)
                components.html(wordcloud.render_embed(), height=400)
            elif chart_type == "条形图":
                bar_chart = draw_bar_chart(word_counts)
                components.html(bar_chart.render_embed(), height=400)
            elif chart_type == "折线图":
                line_chart = draw_line_chart(word_counts)
                components.html(line_chart.render_embed(), height=400)
            elif chart_type == "饼图":
                pie_chart = draw_pie_chart(word_counts)
                components.html(pie_chart.render_embed(), height=400)
            elif chart_type == "散点图":
                scatter_chart = draw_scatter_chart(word_counts)
                components.html(scatter_chart.render_embed(), height=400)
            elif chart_type == "箱线图":
                boxplot_chart = draw_boxplot_chart(word_counts)
                components.html(boxplot_chart.render_embed(), height=400)
            elif chart_type == "雷达图":
                radar_chart = draw_radar_chart(word_counts)
                components.html(radar_chart.render_embed(), height=400)


if __name__ == "__main__":
    main()
