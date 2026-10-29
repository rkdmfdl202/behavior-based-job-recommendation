import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title='개인화 채용공고 추천 프로토타입',
    page_icon='💼',
    layout='wide'
)

st.markdown('''
<style>
    .block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 4rem;}
    .hero {
        position: relative;
        overflow: hidden;
        padding: 38px 40px 34px 40px;
        border-radius: 28px;
        background:
          radial-gradient(circle at 85% 20%, rgba(255,255,255,.16), transparent 24%),
          radial-gradient(circle at 72% 82%, rgba(168,85,247,.25), transparent 26%),
          linear-gradient(135deg, #0f172a 0%, #312e81 48%, #7c3aed 100%);
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 24px 60px rgba(49,46,129,.22);
    }
    .hero:after {
        content:'';
        position:absolute;
        width:220px;
        height:220px;
        border-radius:50%;
        right:-70px;
        top:-70px;
        background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.12);
    }
    .hero-eyebrow {
        display:inline-block;
        padding:7px 11px;
        border-radius:999px;
        background:rgba(255,255,255,.12);
        border:1px solid rgba(255,255,255,.16);
        color:#e9d5ff;
        font-size:12px;
        font-weight:700;
        letter-spacing:.04em;
        margin-bottom:14px;
    }
    .hero h1 {
        margin:0 0 12px 0;
        font-size: 42px;
        line-height:1.15;
        letter-spacing:-.03em;
    }
    .hero p {
        margin:0 0 22px 0;
        max-width:760px;
        color: rgba(255,255,255,.82);
        font-size: 16px;
        line-height:1.7;
    }
    .hero-grid {
        display:grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        gap:10px;
        max-width:820px;
    }
    .hero-stat {
        padding:12px 14px;
        border-radius:16px;
        background:rgba(255,255,255,.10);
        border:1px solid rgba(255,255,255,.13);
        backdrop-filter: blur(8px);
    }
    .hero-stat-label {
        font-size:11px;
        color:rgba(255,255,255,.65);
        margin-bottom:4px;
    }
    .hero-stat-value {
        font-size:18px;
        font-weight:800;
        color:white;
    }
    .flow {
        display:flex;
        flex-wrap:wrap;
        align-items:center;
        gap:8px;
        margin-top:18px;
        font-size:12px;
        color:rgba(255,255,255,.75);
    }
    .flow-chip {
        padding:7px 10px;
        border-radius:999px;
        background:rgba(15,23,42,.22);
        border:1px solid rgba(255,255,255,.12);
    }
    @media (max-width: 800px) {
        .hero {padding:28px 22px;}
        .hero h1 {font-size:32px;}
        .hero-grid {grid-template-columns: repeat(2, minmax(0,1fr));}
    }
    .profile-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(15,23,42,.05);
        height: 100%;
    }
    .profile-label {color:#6b7280; font-size:13px; margin-bottom:6px;}
    .profile-value {font-size:25px; font-weight:700; color:#111827;}
    .job-card {
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 22px 24px;
        margin-bottom: 16px;
        background: #ffffff;
        box-shadow: 0 8px 24px rgba(15,23,42,.05);
    }
    .rank {
        display:inline-flex; align-items:center; justify-content:center;
        min-width:46px; height:30px; border-radius:999px;
        background:#ede9fe; color:#6d28d9; font-weight:700; font-size:13px;
        margin-bottom:10px;
    }
    .company {color:#6b7280; font-size:14px; margin-bottom:4px;}
    .title {font-size:23px; font-weight:800; color:#111827; margin-bottom:10px;}
    .meta {color:#4b5563; font-size:14px; margin-bottom:12px;}
    .badge {
        display:inline-block; padding:6px 10px; border-radius:999px;
        margin-right:7px; font-size:12px; font-weight:700;
    }
    .badge-purple {background:#f3e8ff; color:#7e22ce;}
    .badge-green {background:#dcfce7; color:#15803d;}
    .badge-blue {background:#dbeafe; color:#1d4ed8;}
    .badge-gray {background:#f3f4f6; color:#4b5563;}
    .section-title {font-size:28px; font-weight:800; margin:28px 0 16px; color:#111827;}
</style>
''', unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
USER_FILE = BASE_DIR / 'user_behavior_app.csv'
REC_FILE = BASE_DIR / 'recommendation_app.csv'

@st.cache_data
def load_data():
    return pd.read_csv(USER_FILE), pd.read_csv(REC_FILE)

def safe_text(value):
    if pd.isna(value):
        return '-'
    text = str(value).strip()
    return text if text else '-'

users, recs = load_data()

available_user_ids = sorted(set(users['user_id'].dropna()) & set(recs['user_id'].dropna()))

st.sidebar.markdown('### 👤 데모 사용자 선택')
selected_user = st.sidebar.selectbox('사용자 ID', available_user_ids, label_visibility='collapsed')
st.sidebar.caption('익명화된 포트폴리오용 샘플 사용자입니다.')

profile = users[users['user_id'] == selected_user].iloc[0]
selected_recs = recs[recs['user_id'] == selected_user].sort_values('rank').head(5)

st.markdown('''
<div class="hero">
  <div class="hero-eyebrow">BEHAVIOR-BASED JOB RECOMMENDATION</div>
  <h1>💼 행동 데이터 기반<br>개인화 채용공고 추천</h1>
  <p>
    최근 30일의 탐색 행동과 실제 지원 이력을 기반으로 관심 직무를 결정하고,
    동일 직무 공고 중 원격근무 가능·연봉 공개 속성을 우선 반영해 TOP5를 추천합니다.
  </p>

  <div class="hero-grid">
    <div class="hero-stat">
      <div class="hero-stat-label">직무 추정 Accuracy</div>
      <div class="hero-stat-value">95.03%</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-label">직무 추정 Coverage</div>
      <div class="hero-stat-value">70.15%</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-label">추천 생성 사용자</div>
      <div class="hero-stat-value">5,495명</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-label">TOP5 충족률</div>
      <div class="hero-stat-value">99.87%</div>
    </div>
  </div>

  <div class="flow">
    <span class="flow-chip">최근 30일 행동</span>
    <span>→</span>
    <span class="flow-chip">관심 직무 결정</span>
    <span>→</span>
    <span class="flow-chip">후보 공고 생성</span>
    <span>→</span>
    <span class="flow-chip">원격·연봉 공개 우선 재정렬</span>
    <span>→</span>
    <span class="flow-chip">TOP5 추천</span>
  </div>
</div>
''', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'''<div class="profile-card"><div class="profile-label">관심 직무</div><div class="profile-value">{safe_text(profile['interest_job_field'])}</div></div>''', unsafe_allow_html=True)
with c2:
    source_raw = safe_text(profile['job_field_source'])
    source_label = '지원 이력 기반' if source_raw == '실제 지원직무' else '최근 탐색 행동 기반'
    st.markdown(f'''<div class="profile-card"><div class="profile-label">직무 판단 근거</div><div class="profile-value">{source_label}</div></div>''', unsafe_allow_html=True)
with c3:
    st.markdown(f'''<div class="profile-card"><div class="profile-label">추천 공고 수</div><div class="profile-value">{len(selected_recs)}개</div></div>''', unsafe_allow_html=True)


if source_raw == '실제 지원직무':
    st.info(
        f"이 사용자의 관심 직무는 최근 검색어가 아니라, 실제 지원 이력에서 확인된 **{safe_text(profile['interest_job_field'])}** 직무를 기준으로 결정되었습니다."
    )
else:
    st.info(
        f"이 사용자는 최근 지원 직무 정보가 없어, 검색어·Specialty·Tag 등 탐색 행동을 바탕으로 **{safe_text(profile['interest_job_field'])}** 직무를 추정했습니다."
    )
st.markdown('<div class="section-title">최근 탐색 행동</div>', unsafe_allow_html=True)
b1, b2, b3 = st.columns(3)
with b1:
    st.markdown(f'''<div class="profile-card"><div class="profile-label">검색어</div><div>{safe_text(profile['recent_keywords'])}</div></div>''', unsafe_allow_html=True)
with b2:
    st.markdown(f'''<div class="profile-card"><div class="profile-label">Specialty</div><div>{safe_text(profile['recent_specialty'])}</div></div>''', unsafe_allow_html=True)
with b3:
    st.markdown(f'''<div class="profile-card"><div class="profile-label">Tag</div><div>{safe_text(profile['recent_tag'])}</div></div>''', unsafe_allow_html=True)

st.markdown('<div class="section-title">⭐ 추천 공고 TOP5</div>', unsafe_allow_html=True)

for _, row in selected_recs.iterrows():
    rank = int(row['rank'])
    title = safe_text(row.get('job_title', row['job_field']))
    company = safe_text(row.get('company_name', 'Demo Company'))
    position = safe_text(row['job_field'])
    remote = safe_text(row['remote_text'])
    salary = safe_text(row['salary_text'])
    cdate = safe_text(row['cdate']).split(' ')[0]
    score = int(row['attribute_score'])

    remote_class = 'badge-green' if remote == '가능' else 'badge-gray'
    salary_class = 'badge-blue' if salary == '공개' else 'badge-gray'
    priority = '<span class="badge badge-purple">우선 추천</span>' if score == 2 else ''

    st.markdown(f'''
    <div class="job-card">
      <div class="rank">TOP {rank}</div>
      <div class="company">{company}</div>
      <div class="title">{title}</div>
      <div class="meta">포지션 · <strong>{position}</strong> &nbsp; | &nbsp; 등록일 · {cdate}</div>
      <span class="badge {remote_class}">🏠 원격근무 {remote}</span>
      <span class="badge {salary_class}">💰 연봉 {salary}</span>
      {priority}
    </div>
    ''', unsafe_allow_html=True)

with st.expander('추천 로직 보기'):
    st.markdown('''
    1. 최근 30일 행동과 실제 지원 이력을 함께 확인  
    2. 실제 지원 직무가 있으면 이를 우선 사용하고, 없으면 탐색 행동으로 관심 직무 추정  
    3. 관심 직무와 동일한 공고만 후보로 생성  
    4. 미래 공고 및 기존 지원 공고 제외  
    5. 원격근무 가능 / 연봉 공개 속성 우선 재정렬  
    6. 동일 점수에서는 최신 공고 우선  
    7. 동일 회사 중복 제거 후 TOP5 추천
    ''')

st.caption('※ 공고명과 회사명은 포트폴리오 시연을 위해 생성한 데모용 예시입니다. 추천 구조와 직무/속성 결과는 익명화된 실제 분석 결과를 기반으로 합니다.')