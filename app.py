import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title='개인화 채용공고 추천 프로토타입',
    page_icon='💼',
    layout='wide'
)

st.title('💼 개인화 채용공고 추천 프로토타입')
st.caption(
    '사용자 행동 데이터로 관심 직무를 결정하고, '
    '원격근무 가능 / 연봉 공개 공고를 우선 재정렬한 TOP5 추천 결과를 보여줍니다.'
)

BASE_DIR = Path(__file__).resolve().parent
USER_FILE = BASE_DIR / 'user_behavior_app.csv'
REC_FILE = BASE_DIR / 'recommendation_app.csv'

@st.cache_data
def load_data():
    users = pd.read_csv(USER_FILE)
    recs = pd.read_csv(REC_FILE)
    return users, recs

def safe_text(value):
    if pd.isna(value):
        return '-'
    value = str(value).strip()
    return value if value else '-'

users, recs = load_data()

available_user_ids = sorted(
    set(users['user_id'].dropna()) &
    set(recs['user_id'].dropna())
)

selected_user = st.sidebar.selectbox(
    '사용자 선택',
    available_user_ids
)

profile = users[users['user_id'] == selected_user].iloc[0]
selected_recs = (
    recs[recs['user_id'] == selected_user]
    .sort_values('rank')
    .head(5)
)

st.subheader('👤 사용자 정보')
c1, c2, c3 = st.columns(3)

with c1:
    st.metric('관심 직무', safe_text(profile['interest_job_field']))
with c2:
    st.metric('직무 결정 방식', safe_text(profile['job_field_source']))
with c3:
    st.metric('추천 공고 수', len(selected_recs))

st.markdown('#### 최근 행동')
b1, b2, b3 = st.columns(3)
with b1:
    st.write('**검색어**')
    st.write(safe_text(profile['recent_keywords']))
with b2:
    st.write('**Specialty**')
    st.write(safe_text(profile['recent_specialty']))
with b3:
    st.write('**Tag**')
    st.write(safe_text(profile['recent_tag']))

st.divider()
st.subheader('⭐ 추천 공고 TOP5')

for _, row in selected_recs.iterrows():
    with st.container(border=True):
        left, right = st.columns([4, 1])

        with left:
            st.markdown(f"### {int(row['rank'])}위 · {safe_text(row['job_field'])}")
            st.write(f"🏠 원격근무: **{safe_text(row['remote_text'])}**")
            st.write(f"💰 연봉 정보: **{safe_text(row['salary_text'])}**")
            st.caption(f"공고 생성일: {safe_text(row['cdate'])}")

        with right:
            if row['attribute_score'] == 2:
                st.success('우선 추천')
            elif row['attribute_score'] == 1:
                st.info('추천')
            else:
                st.caption('일반 추천')

st.divider()

with st.expander('추천 로직 보기'):
    st.markdown(
        '''
        1. 최근 30일 사용자 행동으로 관심 직무 결정  
        2. 관심 직무와 같은 직무 공고만 후보로 생성  
        3. 사용자 기준일 이후 생성된 미래 공고 제외  
        4. 이미 지원한 공고 제외  
        5. 원격근무 가능 / 연봉 공개 공고 우선 재정렬  
        6. 동일 점수에서는 최신 공고 우선  
        7. 동일 회사 중복 최소화  
        8. TOP5 추천
        '''
    )

st.caption('※ 이 앱은 추천 알고리즘 결과를 시각적으로 보여주는 포트폴리오용 프로토타입입니다.')