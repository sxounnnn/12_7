
import streamlit as st

st.set_page_config(
    page_title="편안한 주문",
    page_icon="☕",
    layout="wide"
)

MENU = {
    "따뜻한 아메리카노": ("커피", 3000, "☕"),
    "아이스 아메리카노": ("커피", 3000, "🧊"),
    "카페라떼": ("커피", 3800, "🥛"),
    "바닐라라떼": ("커피", 4300, "🍦"),
    "초코라떼": ("음료", 4200, "🍫"),
    "녹차라떼": ("음료", 4200, "🍵"),
    "레몬차": ("차", 3500, "🍋"),
    "유자차": ("차", 3500, "🍯"),
    "치즈케이크": ("간식", 4500, "🍰"),
    "소금빵": ("간식", 2800, "🥐"),
}

FONT_SIZES = {
    "보통": 18,
    "크게": 24,
    "아주 크게": 30,
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = "menu"

if "notice" not in st.session_state:
    st.session_state.notice = ""

if "font_choice" not in st.session_state:
    st.session_state.font_choice = "크게"

font_size = FONT_SIZES.get(st.session_state.font_choice, 24)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #FFFDF7;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3, p, label {{
        line-height: 1.6;
    }}

    h1, h2, h3 {{
        color: #183B32;
        font-weight: 800;
    }}

    p, label, [data-testid="stMarkdownContainer"] {{
        font-size: {font_size}px;
    }}

    div.stButton > button {{
        min-height: 64px;
        font-size: {font_size}px;
        font-weight: bold;
        border-radius: 14px;
        border: 2px solid #A7C5AE;
        white-space: normal;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #176B4D;
        color: white;
        border-color: #176B4D;
    }}

    .menu-card {{
        background: white;
        border: 2px solid #D9E4D9;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 8px;
    }}

    .menu-name {{
        font-size: {font_size + 2}px;
        font-weight: 800;
        color: #183B32;
    }}

    .price {{
        font-size: {font_size}px;
        font-weight: bold;
        color: #355B47;
    }}

    .total {{
        background: #183B32;
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: {font_size}px;
        font-weight: bold;
        margin: 12px 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def money(amount):
    return f"{amount:,}원"


def total_price():
    return sum(
        MENU[name][1] * qty
        for name, qty in st.session_state.cart.items()
    )


def total_count():
    return sum(st.session_state.cart.values())


def add_item(name):
    st.session_state.cart[name] = (
        st.session_state.cart.get(name, 0) + 1
    )
    st.session_state.notice = f"{name} 메뉴를 담았습니다."


def remove_item(name):
    qty = st.session_state.cart.get(name, 0)

    if qty <= 1:
        st.session_state.cart.pop(name, None)
    else:
        st.session_state.cart[name] = qty - 1


def cancel_order():
    st.session_state.cart = {}
    st.session_state.page = "menu"
    st.session_state.notice = "주문을 취소했습니다."


header, font_col = st.columns([3, 2])

with header:
    st.title("☕ 편안한 주문")
    st.write("천천히 읽고, 편하게 눌러 주세요.")

with font_col:
    st.radio(
        "글씨 크기",
        list(FONT_SIZES.keys()),
        horizontal=True,
        key="font_choice",
    )

st.markdown(
    f"""
    <div class="menu-card">
        <strong>현재 주문</strong><br>
        선택한 메뉴: {total_count()}개<br>
        총금액: {money(total_price())}
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.notice:
    st.info(st.session_state.notice)

steps = {
    "menu": "1. 메뉴 선택",
    "review": "2. 주문 확인",
    "done": "3. 주문 완료",
}

st.subheader(f"현재 단계: {steps[st.session_state.page]}")
st.divider()


if st.session_state.page == "menu":
    st.header("무엇을 드시겠어요?")

    category = st.radio(
        "메뉴 종류를 선택하세요",
        ["전체", "커피", "음료", "차", "간식"],
        horizontal=True,
        key="category",
    )

    items = [
        name for name, data in MENU.items()
        if category == "전체" or data[0] == category
    ]

    for i in range(0, len(items), 2):
        cols = st.columns(2, gap="large")

        for col, name in zip(cols, items[i:i + 2]):
            category_name, price, emoji = MENU[name]

            with col:
                qty = st.session_state.cart.get(name, 0)

                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div class="menu-name">{emoji} {name}</div>
                        <div class="price">{money(price)}</div>
                        <div>선택 수량: {qty}개</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"＋ {name} 담기",
                    key=f"add_{name}",
                    use_container_width=True,
                ):
                    add_item(name)
                    st.rerun()

    st.divider()

    if st.session_state.cart:
        st.markdown(
            f'<div class="total">총금액: {money(total_price())}</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        with left:
            if st.button(
                "주문 내용 확인하기 →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.page = "review"
                st.session_state.notice = ""
                st.rerun()

        with right:
            if st.button(
                "전체 주문 취소",
                use_container_width=True,
            ):
                cancel_order()
                st.rerun()
    else:
        st.info("원하는 메뉴의 담기 버튼을 눌러 주세요.")


elif st.session_state.page == "review":
    st.header("주문 내용을 확인해 주세요")
    st.write("수량이 맞는지 확인하세요. 잘못 선택했다면 수정할 수 있습니다.")

    if not st.session_state.cart:
        st.warning("선택한 메뉴가 없습니다.")

        if st.button("메뉴 선택으로 돌아가기"):
            st.session_state.page = "menu"
            st.rerun()

    else:
        for name in list(st.session_state.cart.keys()):
            qty = st.session_state.cart[name]
            price = MENU[name][1]
            emoji = MENU[name][2]

            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])

            with c1:
                st.markdown(f"### {emoji} {name}")
                st.write(f"{money(price)} × {qty}개")
                st.write(f"소계: {money(price * qty)}")

            with c2:
                if st.button("−", key=f"minus_{name}"):
                    remove_item(name)
                    st.rerun()

            with c3:
                st.markdown(f"**{qty}개**")

            with c4:
                if st.button("＋", key=f"plus_{name}"):
                    add_item(name)
                    st.rerun()

            with c5:
                if st.button("삭제", key=f"delete_{name}"):
                    st.session_state.cart.pop(name, None)
                    st.session_state.notice = f"{name} 메뉴를 삭제했습니다."
                    st.rerun()

            st.divider()

        st.markdown(
            f'<div class="total">최종 금액: {money(total_price())}</div>',
            unsafe_allow_html=True,
        )

        st.warning("연습용 앱입니다. 실제 결제는 진행되지 않습니다.")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("← 메뉴 더 고르기", use_container_width=True):
                st.session_state.page = "menu"
                st.rerun()

        with c2:
            if st.button("주문 전체 취소", use_container_width=True):
                cancel_order()
                st.rerun()

        with c3:
            if st.button(
                "이대로 주문 확인",
                type="primary",
                use_container_width=True,
            ):
                if st.session_state.cart:
                    st.session_state.page = "done"
                    st.session_state.notice = ""
                    st.rerun()
                else:
                    st.error("먼저 메뉴를 선택해 주세요.")


elif st.session_state.page == "done":
    st.success("주문 확인이 완료되었습니다!")
    st.header("최종 주문 내역")

    if st.session_state.cart:
        for name, qty in st.session_state.cart.items():
            emoji = MENU[name][2]
            price = MENU[name][1]

            st.markdown(f"### {emoji} {name} × {qty}개")
            st.write(f"금액: {money(price * qty)}")

        st.markdown(
            f'<div class="total">총 주문 금액: {money(total_price())}</div>',
            unsafe_allow_html=True,
        )

        st.info("시연용 주문입니다. 결제나 매장 전송은 이루어지지 않았습니다.")

        if st.button(
            "새 주문 시작하기",
            type="primary",
            use_container_width=True,
        ):
            cancel_order()
            st.rerun()
    else:
        st.warning("주문 내역이 없습니다.")

        if st.button("처음으로 돌아가기"):
            st.session_state.page = "menu"
            st.rerun()

st.divider()
st.caption("편안한 주문 | 큰 글씨와 쉬운 버튼으로 편리하게")
