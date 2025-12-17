import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("data/netflix_titles.csv")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df = df.dropna(subset=['year_added'])

st.title("📊 Netflix Content Growth Analysis")

# Time-series trend
yearly = df.groupby(['year_added', 'type']).size().reset_index(name='count')

fig = px.line(
    yearly,
    x="year_added",
    y="count",
    color="type",
    markers=True,
    title="Netflix Content Growth Over Time"
)

st.plotly_chart(fig, use_container_width=True)
