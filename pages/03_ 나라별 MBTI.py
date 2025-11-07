# app.py
"""
Streamlit app: MBTI by country
- Reads 'countriesMBTI_16types.csv' from the same folder (or allows upload in the UI)
- Select a country to view MBTI distribution as an interactive Plotly bar chart
- Coloring: highest value (1st) is red; the rest use a smooth gradient

How to deploy on Streamlit Cloud:
1. Put this file (app.py) and 'countriesMBTI_16types.csv' in the repo root.
2. Add requirements.txt (contents included at the bottom of this file).
3. On Streamlit Cloud, point the app to run 'app.py'.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="MBTI by Country", layout="wide")

st.title("🌍 Countries MBTI — 인터랙티브 뷰어")
st.markdown("국가를 선택하면 해당 국가의 MBTI 비율을 깔끔한 Plotly 막대그래프로 보여줍니다.")

# --- load data: prefer local file, otherwise allow upload ---
DEFAULT_CSV = "countriesMBTI_16types.csv"

@st.cache_data
def load_data_from_path(path: str):
    df = pd.read_csv(path)
    return df

uploaded = st.file_uploader("CSV 파일 업로드 (없으면 리포지토리의 countriesMBTI_16types.csv 사용)", type=["csv"]) 

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    if Path(DEFAULT_CSV).exists():
        df = load_data_from_path(DEFAULT_CSV)
    else:
        st.error(f"로컬에 '{DEFAULT_CSV}' 파일이 없습니다. 파일을 업로드 해주세요.")
        st.stop()

# ensure consistent ordering of MBTI columns (Country first)
mbti_cols = [c for c in df.columns if c.lower() != 'country']

# Sidebar controls
with st.sidebar:
    st.header("설정")
    country = st.selectbox("국가 선택", df['Country'].sort_values().tolist())
    sort_option = st.radio("막대 정렬", ("원본 순서", "값 기준 내림차순"))
    show_values = st.checkbox("막대 위에 값 표시", value=True)
    palette_name = st.selectbox("그라데이션 팔레트", ("Plasma", "Viridis", "Cividis", "Inferno"))

# select the row
row = df[df['Country'] == country].iloc[0]
values = [row[c] for c in mbti_cols]

# optionally sort
if sort_option == "값 기준 내림차순":
    order = np.argsort(values)[::-1]
    mbti_ordered = [mbti_cols[i] for i in order]
    values_ordered = [values[i] for i in order]
else:
    mbti_ordered = mbti_cols
    values_ordered = values

n = len(mbti_ordered)

# Build colors: first (max) is red, other bars get gradient
max_idx = int(np.argmax(values_ordered))

# choose palette
palettes = {
    'Plasma': px.colors.sequential.Plasma,
    'Viridis': px.colors.sequential.Viridis,
    'Cividis': px.colors.sequential.Cividis,
    'Inferno': px.colors.sequential.Inferno
}
base_palette = palettes.get(palette_name, px.colors.sequential.Plasma)

# sample base_palette to produce n-1 colors evenly
if len(base_palette) >= (n-1):
    # pick evenly spaced indices
    idxs = np.linspace(0, len(base_palette)-1, n-1).astype(int)
    grad_colors = [base_palette[i] for i in idxs]
else:
    # if palette is small, interpolate by repeating
    grad_colors = [base_palette[i % len(base_palette)] for i in range(n-1)]

# assemble final color list according to position
colors = []
grad_iter = iter(grad_colors)
for i in range(n):
    if i == max_idx:
        colors.append('red')
    else:
        colors.append(next(grad_iter))

# Create Plotly bar chart
fig = go.Figure(go.Bar(
    x=mbti_ordered,
    y=values_ordered,
    marker_color=colors,
    text=[f"{v:.3f}" for v in values_ordered] if show_values else None,
    textposition='auto' if show_values else None,
    hovertemplate='<b>%{x}</b><br>비율: %{y:.3f}<extra></extra>'
))

fig.update_layout(
    title=f"{country} — MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat='.0%g' if (max(values_ordered) <= 1.0) else None,
    template='plotly_white',
    bargap=0.15,
    height=520
)

# If values appear to be proportions like 0.12, convert y-axis to percent display
if df[mbti_cols].max().max() <= 1.0:
    # convert to percent for display but keep original values for hover
    fig.update_traces(y=[v*100 for v in values_ordered], hovertemplate='<b>%{x}</b><br>비율: %{y:.2f}%<extra></extra>')
    fig.update_layout(yaxis_title='비율 (%)')

# show
st.plotly_chart(fig, use_container_width=True)

# small data table
with st.expander("원본 데이터 보기 (선택한 국가)"):
    st.write(pd.DataFrame({"MBTI": mbti_ordered, "Value": values_ordered}).set_index('MBTI'))
    ModuleNotFoundError: No module named 'plotly'

