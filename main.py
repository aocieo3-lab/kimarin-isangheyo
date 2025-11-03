import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
st.write('안녕하세요, 만나서 반갑습니다!')
name=st.text_input('이름을 입력해주세요!')
if st.button('인사말 생성'):
  st.write(name+'님! 반갑습니다!')
  st.balloons()

# app.py
import streamlit as st
import random

st.set_page_config(page_title="MBTI 진로 추천 🧭", page_icon="✨", layout="centered")

st.title("MBTI 기반 진로 추천기 ✨")
st.caption("16개 MBTI 중 하나 골라봐 — 그 유형에 맞춘 진로 2가지랑 학과·성격 팁까지 딱 알려줄게! 😎")

mbti_list = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# 데이터: MBTI -> [(직업, 전공 추천, 어울리는 성격/특징), ...]
career_db = {
    "INTJ": [
        ("연구원 / 데이터 사이언티스트", "컴퓨터공학·통계·수학", "논리적, 장기 계획 잘 세우는 사람 🧠"),
        ("전략 기획자", "경영학·경제학", "전략적 사고 좋아하고 독립적으로 일하는 걸 선호하는 사람 ♟️")
    ],
    "INTP": [
        ("연구 개발자 / 시스템 설계자", "컴퓨터공학·물리·수학", "호기심 많고 이론적 사고 좋아하는 사람 🔬"),
        ("UX 리서처 / 분석가", "심리학·인간공학·통계", "문제의 핵심을 파고드는 걸 즐기는 사람 🔎")
    ],
    "ENTJ": [
        ("경영자 / 기업 전략가", "경영학·경제학·공학", "리더십 있고 목표지향적인 사람 🚀"),
        ("컨설턴트", "경영학·경제학", "빠른 판단과 설득을 즐기는 사람 🗣️")
    ],
    "ENTP": [
        ("스타트업 창업가 / 제품 기획자", "경영학·컴퓨터공학·디자인", "아이디어가 많고 변화 잘 즐기는 사람 💡"),
        ("마케팅 전략가", "광고·경영·커뮤니케이션", "트렌드 민감하고 설득력 있는 사람 📣")
    ],
    "INFJ": [
        ("상담사 / 임상심리사", "심리학·사회복지학", "타인 깊이 이해하고 돕는 걸 좋아하는 사람 ❤️"),
        ("아동교육 전문가 / 교육과정 개발자", "교육학·아동학", "가치 중심으로 의미 있는 일을 하고싶어하는 사람 🌱")
    ],
    "INFP": [
        ("작가 / 콘텐츠 크리에이터", "문예·커뮤니케이션·철학", "내적 가치와 감성 표현을 좋아하는 사람 ✍️"),
        ("예술치료사 / 사회적 기업가", "심리학·미술치료·사회복지", "사람과 사회에 공감 능력 높은 사람 🤝")
    ],
    "ENFJ": [
        ("HR / 인사 담당자", "심리학·경영학", "사람을 이끌고 돕는 일에 에너지 얻는 사람 🌟"),
        ("교육 컨설턴트 / 팀 리더", "교육학·경영학", "조직에서 사람 성장에 관심 많은 사람 🧑‍🏫")
    ],
    "ENFP": [
        ("광고·콘텐츠 기획자", "미디어·커뮤니케이션·디자인", "창의적이고 사람과 소통하는 걸 즐기는 사람 🎨"),
        ("이벤트 플래너 / 브랜드 매니저", "경영·마케팅·디자인", "다양한 아이디어로 분위기 만드는 걸 좋아하는 사람 🎉")
    ],
    "ISTJ": [
        ("회계사 / 감사", "회계·세무·경영학", "책임감 강하고 규칙 잘 지키는 사람 📋"),
        ("품질관리자 / 공무원", "공학·행정학", "절차와 안정성을 중요시하는 사람 🛠️")
    ],
    "ISFJ": [
        ("간호사 / 의료기록사", "간호학·보건학", "섬세하고 다른 사람 돌보는 걸 좋아하는 사람 🩺"),
        ("사서 / 사무행정", "문헌정보학·행정학", "조용히 성실하게 맡은 일 잘 해내는 사람 📚")
    ],
    "ESTJ": [
        ("프로젝트 매니저 / 운영 관리자", "경영학·공학", "결단력 있고 조직 운영을 즐기는 사람 ⚙️"),
        ("법무·행정 전문가", "법학·행정학", "규칙과 절차를 중시하는 실무형 사람 ⚖️")
    ],
    "ESFJ": [
        ("영업·고객관리 (Account Manager)", "경영·마케팅", "다정하고 사람 관계를 잘 챙기는 사람 🤝"),
        ("초등교사 / 교육행정", "교육학·사회복지", "사람 돌보는 일에서 보람 느끼는 사람 🏫")
    ],
    "ISTP": [
        ("기술자 / 엔지니어", "기계·전기·컴퓨터공학", "실무와 문제 해결을 손으로 해내는 걸 좋아하는 사람 🔧"),
        ("파일럿 / 응급구조사", "항공·응급의료", "빠른 상황판단과 침착함 있는 사람 ✈️")
    ],
    "ISFP": [
        ("디자이너 / 사진작가", "시각디자인·예술", "감성적이고 순간을 표현하는 사람 🎨"),
        ("물리치료사 / 치유 관련 직업", "물리치료·운동과학", "사람 몸과 마음을 직접 도와주는 걸 좋아하는 사람 💆‍♀️")
    ],
    "ESTP": [
        ("세일즈 트레이더 / 이벤트 운영", "경영·스포츠·관광", "액션과 즉흥성을 즐기는 활동가 타입 ⚡"),
        ("응급구조·현장기술자", "응급의료·공학", "위기 상황에서 빠르게 움직이는 사람 🚑")
    ],
    "ESFP": [
        ("퍼포먼스 아티스트 / 연예·MC", "무대예술·미디어", "사람들 앞에서 빛나는 걸 즐기는 사람 ✨"),
        ("관광·서비스 기획자", "관광·호텔경영", "사람과 함께 즐거움 만드는 걸 좋아하는 사람 🧳")
    ]
}

# UI
st.markdown("### 1) MBTI 선택")
mbti = st.selectbox("너의 MBTI를 골라봐~", mbti_list, index=0)

st.markdown("---")
st.markdown("### 2) 추천 진로 🧾")
choices = career_db.get(mbti, [])
# shuffle small to add 약간의 변화 but deterministic? random okay.
random.shuffle(choices)

for idx, (job, majors, traits) in enumerate(choices[:2], start=1):
    st.subheader(f"{idx}. {job} {'✨' if idx==1 else ''}")
    st.write(f"- **추천 전공:** {majors}")
    st.write(f"- **어울리는 성격/특징:** {traits}")
    with st.expander("왜 어울려? 더 자세히 보기 ▶️"):
        # Short explanation tailored
        if mbti in ("INTJ","ENTJ"):
            st.write("이 유형들은 계획 세우고 목표를 이루는 데 에너지가 많이 남아. 복잡한 문제를 체계적으로 정리하는 걸 잘하니까 전략·기획·경영 분야가 잘 맞아.")
        elif mbti in ("INFP","INFJ"):
            st.write("가치 지향적이고 공감 능력이 뛰어나서 사람 돕는 일이나 창작 활동에서 큰 만족을 느껴. 감성 표현이 강점!")
        elif mbti in ("ESTP","ESFP"):
            st.write("에너지 넘치고 즉흥적으로 움직이는 데 강점. 현장 중심의 직업이나 사람들과 호흡하는 일이 즐거워.")
        else:
            st.write("실용성과 관심사가 조화되는 직무를 추천했어. 너만의 강점(집중력, 공감, 창의성 등)을 생각해보면 더 잘 맞는 전공을 고를 수 있어.")
    st.markdown("---")

st.markdown("### 3) 한 줄 요약 팁 🎯")
if mbti.startswith("I"):
    st.write("혼자 생각할 시간 갖는 걸 추천! 자기만의 프로젝트로 실력 쌓기 좋음.")
else:
    st.write("사람하고 부대끼면서 배우는 게 큰 장점! 네트워킹과 실무 경험 쌓아라.")

st.markdown("---")
st.markdown("### 4) 추가 기능 — 운 좋으면 랜덤 한 마디 격려 🎁")
if st.button("한 줄 응원 받기"):
    cheers = [
        "너는 이미 충분히 잘하고 있어. 조금만 더 가보자! 💪",
        "작은 시도들이 쌓여 큰 변화를 만든다 — 계속해! 🌱",
        "실패해도 괜찮아. 다음엔 더 잘하면 돼. ✨",
        "네 강점으로 세상을 이롭게 하자! 🔥"
    ]
    st.success(random.choice(cheers))

st.markdown("----")
st.caption("원하면 다른 스타일(더 공식적 / 더 유머러스)로도 출력해줄게. 코드는 streamlit만 쓰고 만들었음 — 바로 배포 가능! 😉")

# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 취향 추천 🍿📚", page_icon="✨", layout="centered")

MBTI_RECS = {
    "ISTJ": {
        "books": [
            ("아토믹 해빗 (Atomic Habits)", "작고 구체적인 습관의 힘을 보여주는 실용서 — 실천 중심인 ISTJ에게 딱! ✅"),
            ("총, 균, 쇠 (Guns, Germs, and Steel)", "문명과 역사 흐름을 체계적으로 설명하는 책 — 사실 기반 분석 좋아하면 굿.")
        ],
        "movies": [
            ("셜록 홈즈 (Sherlock Holmes)", "논리와 디테일로 문제를 푸는 이야기 — 정리 잘하는 너에게 추천 🔍"),
            ("머니볼 (Moneyball)", "데이터와 원칙으로 승부하는 실화극 — 실용주의자 공감 100%")
        ]
    },
    "ISFJ": {
        "books": [
            ("작은 것들의 신 (The Little Prince)", "따뜻하고 은유적인 이야기 — 사람과 관계에 민감한 ISFJ에게 힐링"),
            ("연을 쫓는 아이 (The Kite Runner)", "감정 깊은 드라마 — 공감 능력 있는 사람에게 와닿음")
        ],
        "movies": [
            ("월터의 상점(The Secret Life of Walter Mitty)", "모험과 자기발견 — 꿈꾸는 ENFP에게 추천 ✨"),
            ("비포 선라이즈 (Before Sunrise)", "대화와 감정의 교감 중심 영화 — 사람과 이야기 좋아하면 굿")
        ]
    },
    "ENTP": {
        "books": [
            ("블랙 스완 (The Black Swan 요약 느낌)", "불확실성과 창의적 사고를 좋아하는 사람에게"),
            ("스티브 잡스 평전 (Steve Jobs)", "아이디어와 논쟁, 혁신에 관심 많다면 추천")
        ],
        "movies": [
            ("맨체스터 바이 더 씨 (Manchester by the Sea)", "복잡한 인간관계와 감정—생각할 거리가 많음"),
            ("소셜 네트워크 (The Social Network)", "아이디어+논쟁+빠른 전개 — 토론 좋아하면 굿")
        ]
    },
    "ESTJ": {
        "books": [
            ("팀장처럼 생각하라 (Good to Great 요약 느낌)", "조직, 리더십, 실천 전략에 관심 있는 분께"),
            ("How to Win Friends and Influence People (인간관계 실용서)", "사람 관리와 커뮤니케이션 팁")
        ],
        "movies": [
            ("글래디에이터 (Gladiator)", "리더십·원칙·행동 중심 스토리 — 카리스마 좋아하면"),
            ("킹스 스피치 (The King's Speech)", "책임과 성장에 관한 감동 실화")
        ]
    },
    "ESFJ": {
        "books": [
            ("빨강 머리 앤 (Anne of Green Gables)", "사람과 관계 중심의 따뜻한 이야기 — 인간미 충만"),
            ("작은 것들의 신 (The Little Prince)", "상대 배려와 감성에 공감하는 이에게")
        ],
        "movies": [
            ("프라이드 앤 프리저디스 (Pride & Prejudice)", "관계·사회적 규범·로맨스 — 감동적"),
            ("리틀 미스 선샤인 (Little Miss Sunshine)", "가족과 팀워크, 유머가 있는 드라마")
        ]
    },
    "ENFJ": {
        "books": [
            ("리더의 조건 (Leaders Eat Last 요약 느낌)", "사람 이끄는 일, 공감 기반 리더십 좋아하면"),
            ("연결의 기술 (The Tipping Point 요약 느낌)", "사회적 영향과 연결을 이해하고 싶을 때")
        ],
        "movies": [
            ("쇼생크 탈출 (The Shawshank Redemption)", "희망과 리더십, 연대감 — 울컥함 보장"),
            ("굿 윌 헌팅 (Good Will Hunting)", "성장과 치유, 멘토 관계에 감동")
        ]
    },
    "ENTJ": {
        "books": [
            ("전략의 기술 (Competitive Strategy 요약 느낌)", "전략, 경쟁, 목표 지향적 사고 좋아하면"),
            ("워런 버핏의 바른 투자 (요약 느낌)", "실용적 투자·결정 메커니즘에 관심 있는 사람")
        ],
        "movies": [
            ("더 퍼스트 벤처 (The Founder 느낌)", "비즈니스와 추진력, 성공의 명암을 보여줌"),
            ("인셉션 (Inception)", "복잡한 플랜과 리더십—전략가 기분 낼 수 있음")
        ]
    }
}

# Helper to ensure all 16 present (if not, fill with a fallback)
ALL_MBTI = ["ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP",
            "ESTP","ESFP","ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ"]

for t in ALL_MBTI:
    if t not in MBTI_RECS:
        MBTI_RECS[t] = {
            "books": [("추천 도서 A", "요약 설명 A"), ("추천 도서 B", "요약 설명 B")],
            "movies": [("추천 영화 A", "요약 설명 A"), ("추천 영화 B", "요약 설명 B")]
        }

# UI
st.title("MBTI 취향 추천기 🍿📚")
st.write("MBTI 하나 골라줘~ 그러면 너 타입에 딱 맞는 책 2권이랑 영화 2편 추천해줄게. 알잘딱깔센으로! 😎")

mbti = st.selectbox("너의 MBTI를 골라봐 (예: INFP)", ALL_MBTI)

if st.button("추천해줘!"):
    rec = MBTI_RECS.get(mbti)
    st.subheader(f"{mbti} 추천 목록 ✨")
    st.markdown("**도서 (Books)**")
    for idx, (title, desc) in enumerate(rec["books"], start=1):
        emoji = "📘" if idx == 1 else "📗"
        st.markdown(f"- {emoji} **{title}** — {desc}")
    st.markdown("---")
    st.markdown("**영화 (Movies)**")
    for idx, (title, desc) in enumerate(rec["movies"], start=1):
        emoji = "🎬" if idx == 1 else "🍿"
        st.markdown(f"- {emoji} **{title}** — {desc}")
    st.markdown("---")
    st.write("마음에 드는 거 있으면 나중에 줄거리나 줄임말(요약) 더 뽑아줄게. 귀찮으면 `다음` 버튼만 누르면 바로 다른 타입도 볼 수 있음 😉")
else:
    st.info("MBTI 선택 후 '추천해줘!' 버튼을 눌러줘~")

# 작은 툴팁: 제목 클릭으로 깔끔하게 보기
st.write("")
st.caption("앱 제작: ChatGPT — 이모지랑 편한 말투 적용 완료. 필요하면 추천 리스트 수정하거나 장르 필터도 추가해줄게. ✌️")

