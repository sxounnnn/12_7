import streamlit as st

st.set_page_config(
    page_title="쉬운 키오스크 교실",
    page_icon="🌷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- 큰 글씨와 쉬운 화면 ----------
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Malgun Gothic", "Apple SD Gothic Neo",
        sans-serif;
    }
    .stApp {
        background-color: #FFFDF5;
    }
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    h1 {
        color: #173F35 !important;
        font-size: 2.25rem !important;
        line-height: 1.4 !important;
    }
    h2 {
        color: #173F35 !important;
        font-size: 1.8rem !important;
        line-height: 1.5 !important;
    }
    h3 {
        color: #173F35 !important;
        font-size: 1.45rem !important;
    }
    p, li, label, .stMarkdown {
        font-size: 1.18rem;
        line-height: 1.85;
    }
    div.stButton > button {
        min-height: 64px;
        width: 100%;
        border-radius: 14px;
        border: 2px solid #276749;
        background-color: #FFFFFF;
        color: #173F35;
        font-size: 1.2rem;
        font-weight: 700;
        white-space: normal;
    }
    div.stButton > button:hover {
        background-color: #E6F4EA;
        border-color: #173F35;
        color: #173F35;
    }
    div[data-testid="stAlert"] {
        font-size: 1.1rem;
        border-radius: 12px;
    }
    div[role="radiogroup"] label {
        font-size: 1.15rem !important;
        padding-top: 8px;
        padding-bottom: 8px;
    }
    .welcome {
        background: #E6F4EA;
        padding: 24px;
        border-radius: 18px;
        border-left: 8px solid #276749;
        margin-bottom: 18px;
    }
    .tip {
        background: #FFF0CC;
        padding: 18px;
        border-radius: 14px;
        margin: 12px 0;
        color: #4A3510;
        font-size: 1.15rem;
        line-height: 1.8;
    }
    .small-note {
        color: #454545;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 연습 내용 ----------
ORDER_STEPS = [
    {
        "title": "1단계. 주문 시작하기",
        "emoji": "👆",
        "description": "화면에서 '주문하기' 또는 '시작하기' 버튼을 찾아 눌러 보세요.",
        "tip": "글씨가 작다면 화면을 천천히 살펴보세요. 급하게 누르지 않아도 됩니다.",
    },
    {
        "title": "2단계. 메뉴 고르기",
        "emoji": "🍔",
        "description": "먹고 싶은 햄버거나 음료 사진을 눌러 보세요.",
        "tip": "사진과 메뉴 이름을 함께 확인하면 실수를 줄일 수 있습니다.",
    },
    {
        "title": "3단계. 수량 확인하기",
        "emoji": "🔢",
        "description": "몇 개를 주문할지 정하고, 수량이 맞는지 확인하세요.",
        "tip": "한 개만 필요하다면 수량이 1개인지 확인하세요.",
    },
    {
        "title": "4단계. 주문 내용 확인하기",
        "emoji": "🧾",
        "description": "고른 메뉴와 개수, 전체 금액을 천천히 확인하세요.",
        "tip": "잘못 골랐다면 결제하기 전에 메뉴를 수정하거나 취소하세요.",
    },
    {
        "title": "5단계. 결제 방법 고르기",
        "emoji": "💳",
        "description": "화면에서 카드 결제 등 가능한 결제 방법을 선택하세요.",
        "tip": "기계마다 결제 방법과 카드 넣는 곳이 다를 수 있습니다.",
    },
    {
        "title": "6단계. 주문 완료 확인하기",
        "emoji": "🎉",
        "description": "결제가 끝났다는 안내나 주문 번호가 나왔는지 확인하세요.",
        "tip": "영수증이나 주문 번호를 확인하고, 음식이 나올 때까지 기다리세요.",
    },
]

HELP_TOPICS = {
    "잘못 눌렀어요": (
        "너무 걱정하지 마세요.",
        [
            "화면에 '이전' 또는 '취소' 버튼이 있는지 찾아보세요.",
            "결제하기 전이라면 메뉴를 다시 선택할 수 있는 경우가 많습니다.",
            "결제가 되었는지 모르겠다면 같은 주문을 반복하지 말고 직원에게 물어보세요.",
        ],
    ),
    "카드 결제가 어려워요": (
        "화면의 안내를 한 단계씩 따라가세요.",
        [
            "먼저 카드 결제를 선택하세요.",
            "화면이나 카드 단말기에 표시된 안내를 확인하세요.",
            "카드를 넣거나 대는 위치는 기계마다 다릅니다.",
            "결제 오류가 나면 카드를 반복해서 넣기보다 직원에게 도움을 요청하세요.",
        ],
    ),
    "주문이 끝났는지 모르겠어요": (
        "주문 완료 화면을 확인해 보세요.",
        [
            "'주문이 완료되었습니다'라는 문구가 있는지 확인하세요.",
            "주문 번호나 영수증이 나왔는지 살펴보세요.",
            "확실하지 않으면 추가 주문을 하지 말고 직원에게 확인하세요.",
        ],
    ),
    "직원에게 도움을 받고 싶어요": (
        "도움을 요청해도 괜찮습니다.",
        [
            "주변 직원에게 손을 들어 알려 주세요.",
            "아래 문장을 그대로 말씀하셔도 됩니다.",
        ],
    ),
}


def show_header():
    st.title("🌷 쉬운 키오스크 교실")
    st.markdown(
        '<div class="small-note">어르신을 위한 쉬운 주문 연습</div>',
        unsafe_allow_html=True,
    )


def show_home():
    st.markdown(
        """
        <div class="welcome">
            <h2>반갑습니다! 😊</h2>
            <p>키오스크가 처음이셔도 괜찮습니다.</p>
            <p>천천히 읽고, 큰 버튼을 눌러 보세요.</p>
            <p><b>실제 돈이 결제되지 않는 연습용 앱입니다.</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("무엇을 배우고 싶으세요?")
    if st.button("🍔 1. 주문하는 방법 배우기", key="home_order"):
        st.session_state.page = "주문 연습"
        st.session_state.order_step = 0
        st.rerun()

    if st.button("💳 2. 카드 결제 방법 알아보기", key="home_pay"):
        st.session_state.page = "결제 안내"
        st.rerun()

    if st.button("🙋 3. 어려운 상황 해결하기", key="home_help"):
        st.session_state.page = "문제 해결"
        st.rerun()

    if st.button("🧠 4. 배운 내용 확인하기", key="home_quiz"):
        st.session_state.page = "확인 문제"
        st.rerun()

    st.markdown(
        """
        <div class="tip">
        💚 <b>기억하세요!</b><br>
        서두르지 않아도 됩니다. 잘 모르겠으면 직원에게 도움을 요청하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_order_practice():
    st.header("🍔 주문 따라 하기")
    st.write("아래 안내를 읽고, 다음 버튼을 눌러 보세요.")

    if "order_step" not in st.session_state:
        st.session_state.order_step = 0

    step = st.session_state.order_step
    total = len(ORDER_STEPS)
    st.progress((step + 1) / total, text=f"전체 {total}단계 중 {step + 1}단계")

    data = ORDER_STEPS[step]
    st.subheader(f"{data['emoji']} {data['title']}")
    st.markdown(
        f"""
        <div class="welcome">
            <p>{data['description']}</p>
        </div>
        <div class="tip">
            💡 <b>도움말</b><br>{data['tip']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        if st.button("⬅️ 이전 단계", disabled=(step == 0), key="order_prev"):
            st.session_state.order_step -= 1
            st.rerun()

    with right:
        if step < total - 1:
            if st.button("다음 단계 ➡️", key="order_next"):
                st.session_state.order_step += 1
                st.rerun()
        else:
            if st.button("🎉 처음부터 다시 연습하기", key="order_restart"):
                st.session_state.order_step = 0
                st.rerun()

    if step == total - 1:
        st.success("축하합니다! 주문 순서를 모두 배우셨습니다.")


def show_payment():
    st.header("💳 카드 결제 안내")
    st.write("카드 결제는 기계마다 조금씩 다릅니다. 아래 순서를 참고하세요.")

    payment_steps = [
        ("1. 결제 방법 선택", "화면에서 '카드' 또는 '카드 결제'를 선택합니다."),
        ("2. 카드 위치 찾기", "화면이나 단말기에 카드 삽입·접촉 위치가 표시되는지 확인합니다."),
        ("3. 화면 안내 따르기", "카드를 넣거나 대고, 필요하면 화면의 추가 안내를 따릅니다."),
        ("4. 결제 결과 확인", "승인 완료 메시지나 주문 완료 화면을 확인합니다."),
    ]

    for title, detail in payment_steps:
        with st.expander(title, expanded=True):
            st.write(detail)

    st.markdown(
        """
        <div class="tip">
        ⚠️ <b>꼭 기억하세요</b><br>
        비밀번호 입력이나 결제 과정이 헷갈리면 주변 직원에게 도움을 요청하세요.
        카드와 비밀번호를 다른 사람에게 함부로 맡기지 마세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_help():
    st.header("🙋 어려운 상황 해결하기")
    st.write("지금 겪고 있는 상황을 골라 보세요.")

    topic = st.selectbox(
        "어떤 점이 어려우신가요?",
        list(HELP_TOPICS.keys()),
    )
    title, instructions = HELP_TOPICS[topic]

    st.subheader(title)
    for item in instructions:
        st.markdown(f"- {item}")

    if topic == "직원에게 도움을 받고 싶어요":
        st.markdown(
            """
            <div class="welcome">
                <h3>이렇게 말씀해 보세요.</h3>
                <p><b>"죄송하지만, 키오스크 사용을 도와주시겠어요?"</b></p>
                <p><b>"카드 결제하는 방법을 알려 주세요."</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_quiz():
    st.header("🧠 배운 내용 확인하기")
    st.write("문제를 읽고 정답 하나를 골라 보세요.")

    questions = [
        {
            "question": "1. 메뉴를 잘못 골랐다면 언제 확인하는 것이 좋을까요?",
            "options": [
                "결제하기 전에 주문 내용을 확인한다",
                "무조건 다시 결제한다",
                "확인하지 않고 나간다",
            ],
            "answer": "결제하기 전에 주문 내용을 확인한다",
            "explanation": "결제하기 전에 메뉴와 금액을 확인하면 실수를 줄일 수 있습니다.",
        },
        {
            "question": "2. 결제가 되었는지 모르겠다면 어떻게 할까요?",
            "options": [
                "바로 같은 주문을 다시 한다",
                "직원에게 결제 여부를 확인해 달라고 한다",
                "카드를 계속 넣었다 뺀다",
            ],
            "answer": "직원에게 결제 여부를 확인해 달라고 한다",
            "explanation": "중복 결제를 막기 위해 먼저 결제 여부를 확인하세요.",
        },
        {
            "question": "3. 키오스크 사용이 어려울 때 가장 좋은 방법은 무엇일까요?",
            "options": [
                "당황해서 아무 버튼이나 누른다",
                "도움을 요청하지 않는다",
                "직원에게 도움을 요청한다",
            ],
            "answer": "직원에게 도움을 요청한다",
            "explanation": "도움을 요청하는 것은 자연스러운 일입니다. 천천히 하셔도 됩니다.",
        },
    ]

    with st.form("quiz_form"):
        answers = []
        for index, question in enumerate(questions):
            st.markdown(f"### {question['question']}")
            answer = st.radio(
                "답을 선택하세요.",
                question["options"],
                index=None,
                key=f"quiz_{index}",
            )
            answers.append(answer)

        submitted = st.form_submit_button("정답 확인하기")

    if submitted:
        score = 0
        for index, question in enumerate(questions):
            if answers[index] == question["answer"]:
                score += 1

        st.subheader(f"결과: {score} / {len(questions)} 문제 정답")

        for index, question in enumerate(questions):
            if answers[index] == question["answer"]:
                st.success(f"{index + 1}번: 정답입니다! {question['explanation']}")
            else:
                st.info(
                    f"{index + 1}번 정답: {question['answer']}\n\n"
                    f"설명: {question['explanation']}"
                )

        if score == len(questions):
            st.balloons()
            st.success("모든 문제를 맞히셨습니다! 참 잘하셨습니다.")
        else:
            st.write("괜찮습니다. 설명을 다시 읽고 천천히 도전해 보세요.")


# ---------- 앱 실행 ----------
def main():
    try:
        show_header()

        if "page" not in st.session_state:
            st.session_state.page = "처음 화면"
        if "order_step" not in st.session_state:
            st.session_state.order_step = 0

        pages = [
            "처음 화면",
            "주문 연습",
            "결제 안내",
            "문제 해결",
            "확인 문제",
        ]

        selected = st.radio(
            "배우고 싶은 메뉴를 선택하세요.",
            pages,
            horizontal=False,
            key="page_navigation",
            label_visibility="collapsed",
        )

        # 첫 화면의 큰 버튼으로 이동한 경우에도 선택 메뉴를 동기화합니다.
        if selected != st.session_state.page:
            st.session_state.page = selected

        st.divider()

        if st.session_state.page == "처음 화면":
            show_home()
        elif st.session_state.page == "주문 연습":
            show_order_practice()
        elif st.session_state.page == "결제 안내":
            show_payment()
        elif st.session_state.page == "문제 해결":
            show_help()
        elif st.session_state.page == "확인 문제":
            show_quiz()
        else:
            st.session_state.page = "처음 화면"
            show_home()

        st.divider()
        st.caption(
            "쉬운 키오스크 교실 · 교육용 연습 앱 · 실제 주문이나 결제는 진행하지 않습니다."
        )

    except Exception:
        st.error(
            "화면을 표시하는 중 문제가 발생했습니다. "
            "페이지를 새로고침한 뒤 다시 이용해 주세요."
        )


if __name__ == "__main__":
    main()
