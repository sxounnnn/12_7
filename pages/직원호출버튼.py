
import streamlit as st

st.set_page_config(
    page_title="딩동 | 직원 호출",
    page_icon="🔔",
    layout="centered",
)

TABLES = [f"{i}번 테이블" for i in range(1, 21)]

REQUESTS = [
    "직원 호출",
    "물 요청",
    "추가 주문",
    "식기 요청",
    "계산 요청",
    "기타 요청",
]

st.markdown("""
<style>
.main .block-container {
    max-width: 600px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(135deg, #fff0e5, #ffdcc8);
    padding: 30px 15px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    color: #963b1c;
    font-size: 38px;
}
.hero p {
    color: #704a3b;
}
div.stButton > button[kind="primaryFormSubmit"] {
    min-height: 55px;
    font-size: 19px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🔔 딩동!</h1>
    <p>필요하실 때 편하게 직원을 호출해 주세요.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🙋 직원 호출하기")

with st.form("call_form"):
    table = st.selectbox("테이블 번호", TABLES)
    request = st.selectbox("요청 사항", REQUESTS)

    submitted = st.form_submit_button(
        "🔔 직원 호출하기",
        type="primary",
        use_container_width=True,
    )

if submitted:
    st.success(
        f"{table}에서 '{request}' 요청을 선택했어요!"
    )
    st.info(
        "이 화면은 호출 요청을 확인하는 예시입니다. "
        "직원에게 실제로 전달하려면 공용 데이터베이스와 "
        "직원 알림 기능을 연결해야 합니다."
    )

st.divider()
st.caption("편안한 식사를 위해 언제든 호출해 주세요 😊")
