
import streamlit as st

st.set_page_config(
    page_title="딩동! 직원 호출",
    page_icon="🔔",
    layout="centered",
)

st.markdown("""
<style>
.main .block-container {
    max-width: 620px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(135deg, #fff2e5, #ffdec9);
    padding: 28px 14px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    color: #943917;
    font-size: 40px;
    margin-bottom: 8px;
}
.hero p {
    color: #704a3b;
    margin: 0;
    font-size: 17px;
}
div.stButton > button {
    min-height: 58px;
    border-radius: 12px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🔔 딩동!</h1>
    <p>무엇을 도와드릴까요?</p>
</div>
""", unsafe_allow_html=True)

st.subheader("필요한 도움을 선택해 주세요")

requests_list = [
    ("🙋 직원 호출", "직원 호출"),
    ("🖥️ 키오스크 사용 도움", "키오스크 사용 도움"),
    ("💳 결제 도움", "결제 도움"),
    ("🍽️ 주문 관련 문의", "주문 관련 문의"),
]

if "selected_request" not in st.session_state:
    st.session_state.selected_request = "직원 호출"

for start in range(0, len(requests_list), 2):
    cols = st.columns(2)

    for offset, (label, value) in enumerate(
        requests_list[start:start + 2]
    ):
        with cols[offset]:
            selected = (
                st.session_state.selected_request == value
            )

            if st.button(
                ("✅ " if selected else "") + label,
                key=f"request_{start + offset}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_request = value
                st.rerun()

st.write("")

st.caption(
    f"선택한 요청: {st.session_state.selected_request}"
)

if st.button(
    "🔔 직원 호출하기",
    type="primary",
    use_container_width=True,
):
    st.session_state.call_completed = True

if st.session_state.get("call_completed", False):
    st.success("✅ 직원이 호출되었습니다!")
    st.info(
        f"요청 내용: {st.session_state.selected_request}"
    )

st.divider()
st.caption("편안한 식사를 위해 언제든 도움을 요청해 주세요 😊")
