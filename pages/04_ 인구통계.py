# app.py
# Streamlit 앱: 지역구 선택 → 나이(x) vs 인구수(y) 꺾은선 그래프 (Plotly)
# 사용법: Streamlit Cloud에 업로드하거나 로컬에서 `streamlit run app.py` 로 실행.
# population.csv를 같은 디렉토리에 두거나, 업로더로 파일 업로드.

import streamlit as st
import pandas as pd
import plotly.express as px
import io
import re
import uuid

st.set_page_config(page_title="지역구별 연령별 인구수", layout="wide")
st.title("🌆 지역구별 연령별 인구수 — Plotly + Streamlit")
st.markdown("CSV에서 지역구를 골라 `나이`(가로) 대비 `인구수`(세로) 꺾은선 그래프를 그립니다. 다양한 파일 포맷을 자동으로 시도해요.")

# ---------- 데이터 로드 유틸 ----------
@st.cache_data
def try_read_local(paths=None):
    if paths is None:
        paths = ["population.csv", "./population.csv"]
    for p in paths:
        try:
            try:
                df = pd.read_csv(p)
            except Exception:
                df = pd.read_csv(p, encoding="cp949")
            return df
        except FileNotFoundError:
            continue
        except Exception:
            continue
    return None

def safe_read_uploaded(u):
    try:
        return pd.read_csv(u)
    except Exception:
        u.seek(0)
        return pd.read_csv(u, encoding="cp949")

# ---------- 로드 단계 ----------
local_df = try_read_local()
if local_df is None:
    st.info("로컬에서 population.csv 파일을 찾지 못했어요. 파일을 업로드하거나 레포에 올려주세요.")
    uploaded_file = st.file_uploader("CSV 파일 업로드 (예: population.csv)", type=["csv"])
    if uploaded_file is not None:
        df = safe_read_uploaded(uploaded_file)
    else:
        st.stop()
else:
    df = local_df

# ---------- 데이터 미리보기 ----------
st.subheader("데이터 미리보기 (최대 10행)")
st.dataframe(df.head(10))

cols = df.columns.tolist()

# ---------- 사이드바: 컬럼 매핑 ----------
st.sidebar.header("컬럼 매핑")
def recommend(keywords):
    for k in keywords:
        for c in cols:
            if k.lower() in c.lower():
                return c
    return None

region_default = recommend(["지역구", "구", "지역", "city", "district"]) or cols[0]
age_default = recommend(["나이", "연령", "age", "age_group"]) or (cols[1] if len(cols)>1 else cols[0])
pop_default = recommend(["인구", "population", "pop", "count"]) or (cols[2] if len(cols)>2 else cols[0])

region_col = st.sidebar.selectbox("지역구/행정구 컬럼", options=cols, index=cols.index(region_default))
age_col = st.sidebar.selectbox("나이 컬럼", options=cols, index=cols.index(age_default))
pop_col = st.sidebar.selectbox("인구수 컬럼", options=cols, index=cols.index(pop_default))

# ---------- 선택할 지역 ----------
regions = df[region_col].dropna().unique().tolist()
if len(regions) == 0:
    st.error("선택한 지역 컬럼에 유효한 값이 없습니다. 다른 컬럼을 선택해 주세요.")
    st.stop()

regions_sorted = sorted(regions, key=lambda x: str(x))
selected_region = st.sidebar.selectbox("지역구를 선택하세요", options=regions_sorted)

# ---------- 전처리: 나이 숫자 추출 ----------
def extract_age_number(x):
    # 반환값: 정수 또는 None
    if pd.isna(x):
        return None
    if isinstance(x, (int, float)) and not pd.isna(x):
        try:
            return int(x)
        except Exception:
            return None
    s = str(x).strip()
    # 흔한 패턴 처리: '30대' -> 30, '30-34' -> 30, '30세' -> 30, '30 ~ 34' -> 30
    m = re.search(r"(\d{1,3})", s)
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

# ---------- 안전한 임시 컬럼명 생성 (충돌 방지) ----------
temp_age_col = "__age_num__" + uuid.uuid4().hex[:6]
temp_pop_col = "__pop_num__" + uuid.uuid4().hex[:6]

# ---------- 필터링 및 숫자 변환 ----------
sub = df[df[region_col] == selected_region].copy()
if sub.empty:
    st.warning("선택한 지역에 해당하는 데이터가 없습니다.")
    st.stop()

# age 숫자형 변환
if pd.api.types.is_numeric_dtype(sub[age_col]):
    sub[temp_age_col] = sub[age_col].astype('Int64')
else:
    sub[temp_age_col] = sub[age_col].apply(extract_age_number).astype('Int64')

# population 숫자형 변환 (콤마 제거 등)
def make_numeric_pop(x):
    if pd.isna(x):
        return None
    try:
        s = str(x).replace(",", "").strip()
        # 빈 문자열 -> NaN
        if s == "":
            return None
        return pd.to_numeric(s)
    except:
        return None

sub[temp_pop_col] = sub[pop_col].apply(make_numeric_pop)

# drop rows where temp_age_col or temp_pop_col is null
sub_clean = sub.dropna(subset=[temp_age_col, temp_pop_col]).copy()
if sub_clean.empty:
    st.warning("전처리 결과(나이/인구 변환) 후 유효한 데이터가 없습니다. 컬럼 매핑을 다시 확인하세요.")
    st.stop()

# ---------- 집계: 같은 나이 합계 (as_index=False 로 안전하게) ----------
agg = (
    sub_clean.groupby(temp_age_col, as_index=False)[temp_pop_col]
    .sum()
    .rename(columns={temp_age_col: "age", temp_pop_col: "population"})
)
agg = agg.sort_values(by="age").reset_index(drop=True)

# ---------- 그래프 ----------
st.subheader(f"{selected_region} — 연령별 인구수 (라인 차트)")
fig = px.line(agg, x="age", y="population", markers=True,
              title=f"{selected_region} - 나이별 인구수",
              labels={"age":"나이", "population":"인구수"})
fig.update_layout(template="plotly_white", hovermode="x unified")
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# ---------- 데이터 테이블 및 통계 ----------
st.subheader("집계 데이터")
st.dataframe(agg)

st.subheader("기본 통계")
c1, c2, c3 = st.columns(3)
c1.metric("최소 나이", int(agg['age'].min()))
c2.metric("최대 나이", int(agg['age'].max()))
c3.metric("총 인구수", int(agg['population'].sum()))

# ---------- 다운로드 ----------
@st.cache_data
def to_csv_bytes(df_):
    buf = io.StringIO()
    df_.to_csv(buf, index=False)
    return buf.getvalue().encode('utf-8')

csv_bytes = to_csv_bytes(agg)
st.download_button("집계 결과 CSV 다운로드", data=csv_bytes, file_name=f"{selected_region}_age_population.csv", mime="text/csv")

st.markdown("---")
st.caption("※ 컬럼 이름이 다양할 수 있으니 사이드바에서 정확한 컬럼을 선택해주세요. 나이 형식이 다양해도 첫 숫자(ex: '30대'->30, '30-34'->30)를 기준으로 집계합니다.")
