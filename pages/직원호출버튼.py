
import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="딩동! 직원 호출",
    page_icon="🔔",
    layout="centered",
)

REQUESTS = [
    ("🙋 직원 호출", "직원 호출"),
    ("🖥️ 키오스크 사용 도움", "키오스크 사용 도움"),
    ("💳 결제 도움", "결제 도움"),
    ("🍽️ 주문 관련 문의", "주문 관련 문의"),
]

# 화면 디자인
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

if "selected_request" not in st.session_state:
    st.session_state.selected_request = "직원 호출"

# 도움 항목을 두 칸씩 표시
for start in range(0, len(REQUESTS), 2):
    cols = st.columns(2)

    for offset, (label, value) in enumerate(
        REQUESTS[start:start + 2]
    ):
        index = start + offset

        with cols[offset]:
            selected = (
                st.session_state.selected_request == value
            )

            if st.button(
                ("✅ " if selected else "") + label,
                key=f"request_{index}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_request = value
                st.rerun()

st.write("")

st.caption(
    f"선택한 요청: **{st.session_state.selected_request}**"
)

# 직원에게 텔레그램 알림 전송
def notify_staff(message):
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
    except Exception:
        return False, (
            "직원 알림 설정이 필요해요. "
            "관리자가 텔레그램 정보를 등록해야 합니다."
        )

    if not token or not chat_id:
        return False, "직원 알림 설정을 확인해 주세요."

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
            },
            timeout=10,
        )
        response.raise_for_status()

        result = response.json()
        if not result.get("ok"):
            return False, "직원 알림 전송에 실패했어요."

        return True, "직원에게 호출을 전달했어요!"

    except (requests.RequestException, ValueError):
        return False, (
            "알림 전송에 실패했어요. "
            "인터넷 연결이나 알림 설정을 확인해 주세요."
        )


# 큰 직원 호출 버튼
if st.button(
    "🔔 직원 호출하기",
    type="primary",
    use_container_width=True,
):
    request_type = st.session_state.selected_request

    now = datetime.now(
        ZoneInfo("Asia/Seoul")
    ).strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "🔔 키오스크 직원 호출\n"
        f"요청 내용: {request_type}\n"
        f"호출 시간: {now}\n"
        "직원의 확인이 필요합니다."
    )

    with st.spinner("직원에게 호출을 전달하고 있어요..."):
        success, result_message = notify_staff(message)

    if success:
        st.success("✅ " + result_message)
        st.info("직원이 확인할 때까지 잠시 기다려 주세요.")
    else:
        st.error("⚠️ " + result_message)

st.divider()
st.caption("편안한 식사를 위해 언제든 도움을 요청해 주세요 😊")
