import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st


# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(
    page_title="딩동 | 직원 호출",
    page_icon="🔔",
    layout="centered",
)

DB_PATH = Path(__file__).with_name("calls.db")

TABLES = [f"{i}번 테이블" for i in range(1, 21)]
REQUESTS = [
    "직원 호출",
    "물 요청",
    "추가 주문",
    "식기 요청",
    "계산 요청",
    "기타 요청",
]


# -------------------------------
# 데이터베이스
# -------------------------------
def get_connection():
    conn = sqlite3.connect(
        str(DB_PATH),
        timeout=10,
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                request TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '대기',
                created_at TEXT NOT NULL
            )
        """)


def add_call(table_name, request):
    """같은 테이블에 같은 요청이 대기 중이면 중복 등록하지 않음."""
    with get_connection() as conn:
        existing = conn.execute(
            """
            SELECT id FROM calls
            WHERE table_name = ?
              AND request = ?
              AND status = '대기'
            LIMIT 1
            """,
            (table_name, request),
        ).fetchone()

        if existing:
            return False

        conn.execute(
            """
            INSERT INTO calls
                (table_name, request, status, created_at)
            VALUES (?, ?, '대기', ?)
            """,
            (
                table_name,
                request,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        return True


def get_calls():
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, table_name, request, status, created_at
            FROM calls
            ORDER BY
                CASE WHEN status = '대기' THEN 0 ELSE 1 END,
                id DESC
            LIMIT 200
            """
        ).fetchall()


def complete_call(call_id):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE calls
            SET status = '완료'
            WHERE id = ? AND status = '대기'
            """,
            (call_id,),
        )


def clear_completed():
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM calls WHERE status = '완료'"
        )


# -------------------------------
# 화면 디자인
# -------------------------------
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 24px;
        border-radius: 20px;
        background: linear-gradient(135deg, #fff1e8, #ffe0d0);
        text-align: center;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: #8f3218;
        margin-bottom: 8px;
    }
    .hero p {
        color: #6d493d;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🔔 딩동!</h1>
        <p>필요하실 때 편하게 직원을 호출해 주세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# DB 초기화 오류가 발생하면 사용자에게 안내
try:
    init_db()
except sqlite3.Error:
    st.error(
        "데이터베이스를 준비하지 못했어요. "
        "잠시 후 다시 접속해 주세요."
    )
    st.stop()


# -------------------------------
# 메뉴
# -------------------------------
mode = st.radio(
    "화면 선택",
    ["🙋 손님 호출 화면", "🧑‍🍳 직원 관리 화면"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()


# -------------------------------
# 손님 호출 화면
# -------------------------------
if mode == "🙋 손님 호출 화면":
    st.subheader("🙋 직원을 호출해 주세요")

    with st.form("call_form"):
        table_name = st.selectbox(
            "테이블 번호",
            TABLES,
        )

        request = st.selectbox(
            "요청 사항",
            REQUESTS,
        )

        submitted = st.form_submit_button(
            "🔔 직원 호출하기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        try:
            added = add_call(table_name, request)

            if added:
                st.success(
                    f"호출 완료! {table_name}에서 "
                    f"'{request}' 요청을 보냈어요."
                )
                st.toast("직원에게 호출이 등록됐어요!")
            else:
                st.info(
                    "같은 요청이 이미 대기 중이에요. "
                    "직원이 확인할 때까지 잠시 기다려 주세요."
                )

        except (sqlite3.Error, OSError):
            st.error(
                "호출을 저장하지 못했어요. "
                "직원에게 직접 알려 주세요."
            )

    st.caption(
        "호출 후 잠시 기다려 주세요. "
        "추가 호출은 기존 요청이 처리된 뒤 이용해 주세요."
    )


# -------------------------------
# 직원 관리 화면
# -------------------------------
else:
    st.subheader("🧑‍🍳 직원 호출 관리")

    # 이 화면 영역만 3초마다 자동으로 다시 실행
    @st.fragment(run_every="3s")
    def staff_dashboard():
        try:
            calls = get_calls()
        except (sqlite3.Error, OSError):
            st.error(
                "호출 내역을 불러오지 못했어요. "
                "잠시 후 다시 시도해 주세요."
            )
            return

        pending = [c for c in calls if c["status"] == "대기"]
        completed = [c for c in calls if c["status"] == "완료"]

        col1, col2 = st.columns(2)

        col1.metric("🔔 대기 중", len(pending))
        col2.metric("✅ 최근 완료 내역", len(completed))

        st.divider()

        st.markdown("### 🔔 처리할 호출")

        if not pending:
            st.success("현재 대기 중인 호출이 없어요!")
        else:
            for call in pending:
                with st.container(border=True):
                    left, right = st.columns([3, 1])

                    with left:
                        st.markdown(
                            f"**{call['table_name']}**"
                        )
                        st.markdown(
                            f"📌 {call['request']}"
                        )
                        st.caption(
                            f"호출 시간: {call['created_at']}"
                        )

                    with right:
                        if st.button(
                            "처리 완료",
                            key=f"done_{call['id']}",
                            use_container_width=True,
                        ):
                            try:
                                complete_call(call["id"])
                                st.toast("호출을 완료 처리했어요.")
                                st.rerun()
                            except sqlite3.Error:
                                st.error(
                                    "완료 처리에 실패했어요."
                                )

        with st.expander("✅ 완료된 호출 내역"):
            if not completed:
                st.caption("완료된 호출이 없어요.")
            else:
                for call in completed:
                    st.write(
                        f"✅ {call['table_name']} · "
                        f"{call['request']} · "
                        f"{call['created_at']}"
                    )

                if st.button(
                    "완료 내역 모두 삭제",
                    type="secondary",
                ):
                    try:
                        clear_completed()
                        st.toast("완료 내역을 삭제했어요.")
                        st.rerun()
                    except sqlite3.Error:
                        st.error("삭제에 실패했어요.")

    staff_dashboard()


st.divider()
st.caption(
    "딩동 직원 호출 시스템 · 호출 내역은 앱의 데이터베이스에 저장됩니다."
)
