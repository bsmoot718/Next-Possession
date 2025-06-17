import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page setup
st.set_page_config(page_title="Next Possession Dashboard", layout="centered")
st.title("🏀 Next Possession: 2025 Playoff Player Dashboard")

# Load CSV safely
csv_file = "player_metrics.csv"
if not os.path.exists(csv_file):
    st.error(f"❌ '{csv_file}' not found. Please upload it.")
    st.stop()

metrics = pd.read_csv(csv_file)
drills = pd.read_csv("drill_library.csv")

# Ensure required TS% columns are available
if not {'PTS', 'FGA', 'FTA'}.issubset(metrics.columns):
    st.error("❌ 'TS%' is missing and cannot be calculated. Please check that 'PTS', 'FGA', and 'FTA' exist.")
    st.stop()

# Compute TS%
metrics['TS%'] = metrics['PTS'] / (2 * (metrics['FGA'] + 0.44 * metrics['FTA']))

# UI Select
player = st.sidebar.selectbox("Choose Player", metrics['Player'].unique())
df_player = metrics[metrics['Player'] == player]
position = df_player['Position'].iloc[0]

# Skill chart setup
skills = ['PTS', 'REB', 'AST', 'TS%']
skill_names = ['Scoring', 'Rebounding', 'Playmaking', 'True Shooting %']

radar_df = pd.DataFrame({
    'Skill': skill_names,
    'Player': df_player[skills].mean().values,
    'Benchmark': [25, 5, 7, 0.58] if position == "Guard" else [22, 10, 4, 0.60]
})


# Summary Table
st.subheader("📊 Playoff Performance Summary")
st.write(df_player[skills].describe().T[['mean']].rename(columns={'mean': 'Average'}))

# Radar Chart
st.subheader("📈 Skill vs Benchmark")
fig_radar = px.line_polar(radar_df.melt(id_vars='Skill'), r='value', theta='Skill', color='variable', line_close=True)
st.plotly_chart(fig_radar)
# Drill Recommendations
st.subheader("🧠 Targeted Drill Recommendations")

# 🧠 Targeted Drill Recommendations


# Manual overrides for KAT and Brunson
if player == "Karl-Anthony Towns":
    target_skills = ['Motor', 'Versatility', 'Shooting', 'Defense']
elif player == "Jalen Brunson":
    target_skills = ['Versatility', 'Defense', 'Decision Making', 'Shooting']
else:
    # Fallback to default benchmark comparison
    target_skills = radar_df[radar_df['Player'] < radar_df['Benchmark']]['Skill'].tolist()

# Filter recommended drills based on skill gap
recommended_drills = drills[drills['Skill'].isin(target_skills)]

if not recommended_drills.empty:
    st.dataframe(recommended_drills[['Skill', 'Drill Name']])
else:
    st.markdown("✅ This player is meeting or exceeding all benchmarks.")


# Scoring Trend
st.subheader("📈 Scoring Trend by Game")
fig_pts = px.line(df_player, x='Game', y='PTS', title=f"{player} - Points per Game", markers=True)
st.plotly_chart(fig_pts)

# TS% Over Games
st.subheader("🎯 True Shooting % by Game")
fig_ts = px.line(df_player, x='Game', y='TS%', title=f"{player} - True Shooting %", markers=True)
st.plotly_chart(fig_ts)

# Rebounding + Assist Bar Chart
st.subheader("📊 Playmaking + Rebounding Impact")
df_player['REBAST'] = df_player['REB'] + df_player['AST']
fig_combo = px.bar(df_player, x='Game', y='REBAST', title=f"{player} - REB + AST per Game")
st.plotly_chart(fig_combo)


# Footer
st.markdown("---")
st.caption("By Brian Smoot II • Crafted to demonstrate fit for the Data Scientist – Basketball role • Merging basketball IQ with data storytelling")






