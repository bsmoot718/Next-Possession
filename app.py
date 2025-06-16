
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
metrics = pd.read_csv("player_metrics.csv")
benchmarks = pd.read_csv("benchmark_data.csv")
drills = pd.read_csv("drill_library.csv")

# Sidebar - Select player
player = st.sidebar.selectbox("Choose Player", metrics['Player'].unique())
df_player = metrics[metrics['Player'] == player]
bm_player = benchmarks[benchmarks['Position'] == df_player['Position'].iloc[0]]

st.title(f"{player} | 2025 Playoffs Player Development Dashboard")

# Summary stats
st.subheader("Playoff Summary")
st.write(df_player.describe().T[['mean']].rename(columns={'mean': 'Average'}))

# Radar chart
st.subheader("Skill Profile vs Benchmark")
skills = ['Scoring', 'Motor', 'Decision Making', 'Defense', 'Shooting', 'Versatility']
radar_df = pd.DataFrame({
    'Skill': skills,
    player: df_player[skills].mean().values,
    'Benchmark': bm_player[skills].values[0]
})
fig = px.line_polar(radar_df.melt(id_vars='Skill'), r='value', theta='Skill', color='variable', line_close=True)
st.plotly_chart(fig)

# Dev Curve
st.subheader("Points Per Game")
fig2 = px.line(df_player, x='Game', y='PTS', title='Scoring Trend')
st.plotly_chart(fig2)

# Drill suggestions
st.subheader("Targeted Drill Suggestions")
gaps = radar_df[radar_df[player] < radar_df['Benchmark']]['Skill']
suggestions = drills[drills['Skill'].isin(gaps)]
st.dataframe(suggestions)
