# FILE: app.py
# Streamlit 앱 (Streamlit Cloud에서 작동하도록 작성)
# 사용법: 이 파일을 repo 루트에 넣고, 같은 디렉토리에 population.csv를 두거나
# Streamlit UI에서 CSV를 업로드하세요.

import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="지역별 연령대 인구 시계열", layout="wide")

st.title("🌆 지역구별 연령별 인구수 — Plotly + Streamlit")
st.markdown("업로드한 CSV에서 지역구를 선택하면 `나이`(가로) 대비 `인구수`(세로) 꺾은선 그래프를 그립니다.")

# 데이터 로드 시도: 먼저 같은 디렉토리의 population.csv를 시도하고, 실패하면 업로더 노출
@st.cache_data
def try_read_local():
    paths = ["population.csv", "./population.csv"]
    for p in paths:
        try:
            # 여러 인코딩 시도
            try:
                df = pd.read_csv(p)
            except Exception:
                df = pd.read_csv(p, encoding='cp949')
            return df
        except FileNotFoundError:
            continue
        except Exception:
            continue
    return None

local_df = try_read_local()

uploaded = None
if local_df is None:
    st.info("로컬에서 population.csv 파일을 찾지 못했어요. 업로드하거나 repos에 추가하세요.")
    uploaded_file = st.file_uploader("CSV 파일 업로드 (예: population.csv)", type=["csv"], accept_multiple_files=False)
    if uploaded_file is not None:
        try:
            # 파일이 text인지 binary인지 자동 처리
            uploaded = pd.read_csv(uploaded_file)
        except Exception:
            uploaded_file.seek(0)
            uploaded = pd.read_csv(uploaded_file, encoding='cp949')

# 최종 df
df = local_df if local_df is not None else uploaded

if df is None:
    st.warning("데이터프레임이 준비되지 않았습니다. 왼쪽에서 CSV를 업로드하거나 repo에 population.csv를 넣어주세요.")
    st.stop()

# 데이터 미리보기와 컬럼 자동 제안
st.subheader("데이터 미리보기")
st.dataframe(df.head(10))

cols = df.columns.tolist()
st.sidebar.subheader("컬럼 매핑 (자동 제안 확인하세요)")

# 자동 제안: '지역', '구', '지역구' 포함 단어 / '나이' / '인구'
def recommend_col(keyword):
    keyword = keyword.lower()
    for c in cols:
        if keyword in c.lower():
            return c
    return None

region_col = st.sidebar.selectbox("지역구/행정구 컬럼", options=cols, index=cols.index(recommend_col('지역구') or recommend_col('구') or cols[0]))
age_col = st.sidebar.selectbox("나이 컬럼", options=cols, index=cols.index(recommend_col('나이') or cols[1] if len(cols)>1 else 0))
pop_col = st.sidebar.selectbox("인구수 컬럼", options=cols, index=cols.index(recommend_col('인구') or recommend_col('population') or cols[2] if len(cols)>2 else 0))

# 선택 가능한 지역 목록 (정렬)
regions = df[region_col].dropna().unique().tolist()
regions_sorted = sorted(regions, key=lambda x: str(x))
selected_region = st.sidebar.selectbox("지역구를 선택하세요", options=regions_sorted)

# 나이형 변환 함수
def to_numeric_age(series):
    # 이미 숫자면 그대로
    if pd.api.types.is_numeric_dtype(series):
        return series.astype(int)
    # 문자열이면 숫자만 뽑기
    def extract_num(x):
        try:
            s = str(x)
            # 흔히 '30대', '30-34', '30' 등 처리
            import re
            m = re.search(r"(\d+)", s)
            if m:
                return int(m.group(1))
            return None
        except Exception:
            return None
    return series.map(extract_num)

# 필터 및 전처리
sub = df[df[region_col] == selected_region].copy()
if sub.empty:
    st.warning("선택한 지역에 해당하는 데이터가 없습니다.")
    st.stop()

sub[age_col+'_num'] = to_numeric_age(sub[age_col])
# 인구수 숫자형 변환
try:
    sub[pop_col+'_num'] = pd.to_numeric(sub[pop_col].astype(str).str.replace(',','').str.strip(), errors='coerce')
except Exception:
    sub[pop_col+'_num'] = pd.to_numeric(sub[pop_col], errors='coerce')

# 집계: 같은 나이대가 여러 행이면 합계
agg = (
    sub.groupby(age_col + '_num', dropna=True)[pop_col + '_num']
    .sum()
    .rename_axis(age_col + '_num_grouped')
    .reset_index(name='population')
)
agg = agg.rename(columns={age_col + '_num_grouped': 'age'})

agg = agg.sort_values(by=age_col+'_num')
agg = agg.rename(columns={age_col+'_num':'age', pop_col+'_num':'population'})

# 그래프 그리기
st.subheader(f"{selected_region} — 연령별 인구수 (라인) 📈")
if agg.empty:
    st.warning("나이/인구 집계 결과가 비어있습니다. 컬럼 매핑을 확인하세요.")
else:
    fig = px.line(agg, x='age', y='population', markers=True, title=f"{selected_region} - 나이별 인구수",
                  labels={'age':'나이', 'population':'인구수'})
    fig.update_layout(template='plotly_white', hovermode='x unified')
    fig.update_traces(mode='lines+markers')
    st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블과 간단한 통계
st.subheader("집계 데이터 (표)")
st.dataframe(agg)

st.subheader("기본 통계")
col1, col2, col3 = st.columns(3)
if not agg.empty:
    col1.metric("최소 나이", int(agg['age'].min()))
    col2.metric("최대 나이", int(agg['age'].max()))
    col3.metric("총 인구수", int(agg['population'].sum()))

# CSV 다운로드
@st.cache_data
def to_csv_bytes(df_):
    buf = io.StringIO()
    df_.to_csv(buf, index=False)
    return buf.getvalue().encode('utf-8')

csv_bytes = to_csv_bytes(agg)
st.download_button("집계 결과 CSV로 다운로드", data=csv_bytes, file_name=f"{selected_region}_age_population.csv", mime='text/csv')

st.markdown("---")
st.caption("※ 컬럼 이름이 다양하게 되어 있는 경우(예: '연령대', 'age_group', 'pop') 사이드바에서 정확한 컬럼을 선택하세요.")


# FILE: requirements.txt
# 복사해서 별도 파일로 저장하세요.
# (아래 내용을 requirements.txt로 저장하면 Streamlit Cloud에서 자동으로 설치됩니다)

# requirements.txt
# streamlit 버전은 필요에 따라 고정하세요. 예시로 최신 호환 버전만 적음
# streamlit
# pandas
# plotly
# 아래는 상용구로 그대로 사용

# -> End of file
