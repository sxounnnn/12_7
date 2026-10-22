
import streamlit as st

# 페이지 기본 설정 (가장 먼저 실행되어야 합니다)
st.set_page_config(
    page_title="시니어 친화형 간편 키오스크",
    page_icon="👵👴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 적용: 시니어 분들을 위한 초대형 글씨 및 큰 버튼 스타일링
st.markdown("""
    <style>
    /* 전체 기본 글자 크기 확대 */
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: bold !important;
    }
    
    /* 일반 텍스트 크기 증가 */
    .big-text {
        font-size: 28px !important;
        line-height: 1.6 !important;
        color: #1E293B;
    }
    
    /* 안내 문구 스타일 */
    .guide-box {
        background-color: #FEF08A;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #EAB308;
        margin-bottom: 25px;
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
    }

    /* 버튼 스타일 커스텀 (Streamlit 기본 버튼 크기 키우기) */
    div.stButton > button {
        font-size: 32px !important;
        font-weight: bold !important;
        padding: 20px 40px !important;
        width: 100% !important;
        border-radius: 20px !important;
        border: 4px solid #3B82F6 !important;
        background-color: #EFF6FF !important;
        color: #1E40AF !important;
        margin-bottom: 15px;
        transition: all 0.2s ease;
    }
    
    /* 빨간색 취소/이전 버튼 스타일 지정용 */
    div.stButton > button:contains("취소"), div.stButton > button:contains("처음으로") {
        border: 4px solid #EF4444 !important;
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
    }
    
    /* 녹색 결제/주문 완료 버튼 스타일 지정용 */
    div.stButton > button:contains("결제"), div.stButton > button:contains("담기") {
        border: 4px solid #10B981 !important;
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
    }

    /* 라디오 버튼 항목 크기 키우기 */
    [data-testid="stMarkdownContainer"] p {
        font-size: 26px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태(State) 초기화 - 주문 정보 저장
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: 메뉴 선택, 2: 옵션 선택, 3: 장바구니 및 확인, 4: 완료
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 샘플 메뉴 데이터 (노인분들이 선호하고 직관적인 메뉴 구성)
MENU_DATA = {
    "☕ 따뜻한 음료": [
        {"name": "아메리카노 (따뜻한 것)", "price": 3000, "desc": "씁쓸하고 깔끔한 기본 커피입니다."},
        {"name": "카페라떼 (우유 커피)", "price": 3500, "desc": "우유가 들어간 부드러운 커피입니다."},
        {"name": "대추차 (건강차)", "price": 4000, "desc": "달콤하고 몸에 좋은 전통 대추차입니다."},
        {"name": "생강차 (건강차)", "price": 4000, "desc": "알싸하고 감기에 좋은 생강차입니다."}
    ],
    "🥤 시원한 음료": [
        {"name": "아이스 아메리카노", "price": 3000, "desc": "얼음이 든 시원한 커피입니다."},
        {"name": "식혜 (시원한 차)", "price": 3500, "desc": "달콤하고 시원한 전통 식혜입니다."},
        {"name": "오미자 에이드", "price": 4000, "desc": "새콤달콤하고 톡 쏘는 음료입니다."}
    ],
    "🥪 주전부리 (간식)": [
        {"name": "단팥빵", "price": 2000, "desc": "달콤한 팥이 듬뿍 든 빵입니다."},
        {"name": "가래떡 구이", "price": 3000, "desc": "조청에 찍어먹는 쫄깃한 떡입니다."}
    ]
}

# 상단 타이틀
st.title("👵👴 어르신을 위한 느린 키오스크")
st.write("---")

# [1단계: 카테고리 및 메뉴 선택]
if st.session_state.step == 1:
    st.markdown('<div class="guide-box">💡 드시고 싶은 종류를 먼저 누른 후, 아래에서 메뉴를 골라주세요.</div>', unsafe_allow_html=True)
    
    # 대형 탭으로 카테고리 분리
    categories = list(MENU_DATA.keys())
    tabs = st.tabs([f"✨ {cat}" for cat in categories])
    
    for idx, tab in enumerate(tabs):
        with tab:
            cat_name = categories[idx]
            st.write(f"### 📍 {cat_name} 메뉴판")
            
            # 메뉴들을 어르신들이 보기 편하게 큰 버튼 형태로 배치
            for item in MENU_DATA[cat_name]:
                button_label = f"👉 {item['name']} ({item['price']:,}원)"
                if st.button(button_label, key=f"btn_{item['name']}"):
                    st.session_state.selected_item = item
                    st.session_state.step = 2
                    st.rerun()

# [2단계: 옵션 선택 및 확인]
elif st.session_state.step == 2:
    item = st.session_state.selected_item
    st.markdown('<div class="guide-box">💡 선택하신 메뉴가 맞는지 확인하시고, 아래 버튼을 눌러주세요.</div>', unsafe_allow_html=True)
    
    st.markdown(f"<div class='big-text'><b>선택하신 메뉴:</b> <span style='color:#1E40AF; font-size:36px;'>{item['name']}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-text'><b>가격:</b> {item['price']:,}원</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-text' style='color:#64748B;'>설명: {item['desc']}</div>", unsafe_allow_html=True)
    st.write("---")
    
    # 실수 방지를 위해 수량을 아주 직관적인 큰 라디오 버튼으로 제공
    st.write("❓ 몇 잔(개) 주문하시겠습니까?")
    quantity = st.radio("수량 선택", [1, 2, 3, 4, 5], index=0, horizontal=True, label_visibility="collapsed")
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ 잘못 골랐어요 (취소)"):
            st.session_state.selected_item = None
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("✅ 먹고 갈래요 (담기)"):
            st.session_state.cart.append({
                "name": item['name'],
                "price": item['price'],
                "quantity": quantity,
                "total": item['price'] * quantity
            })
            st.session_state.step = 3
            st.rerun()

# [3단계: 장바구니 확인 및 최종 결제 결정]
elif st.session_state.step == 3:
    st.markdown('<div class="guide-box">💡 주문하신 내용이 전부 맞나요? 마지막으로 확인해 주세요.</div>', unsafe_allow_html=True)
    
    total_payment = 0
    st.write("### 🛒 내가 고른 주전부리 목록")
    
    # 담긴 상품 목록 출력
    for idx, cart_item in enumerate(st.session_state.cart):
        st.markdown(f"""
            <div class='big-text' style='background-color:#F8FAFC; padding:15px; border-radius:10px; margin-bottom:10px; border-left:6px solid #3B82F6;'>
                <b>• {cart_item['name']}</b> : {cart_item['quantity']}개 → <b>{cart_item['total']:,}원</b>
            </div>
        """, unsafe_allow_html=True)
        total_payment += cart_item['total']
        
    st.write("---")
    st.markdown(f"<div class='big-text' style='text-align:right;'>총 낼 금액: <span style='color:#EF4444; font-size:40px;'>{total_payment:,}원</span></div>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ 메뉴 더 고르기"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("💳 돈 내고 주문하기 (결제)"):
            st.session_state.step = 4
            st.rerun()
            
    # 전체 취소 버튼을 하단에 별도 배치하여 접근성 향상
    if st.button("🚨 처음부터 다시하기 (전체 취소)"):
        st.session_state.cart = []
        st.session_state.selected_item = None
        st.session_state.step = 1
        st.rerun()

# [4단계: 주문 완료 안내]
elif st.session_state.step == 4:
    st.markdown('<div class="guide-box" style="background-color:#DCFCE7; border-color:#22C55E;">🎉 주문이 아주 잘 되었습니다! 고맙습니다.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class='big-text' style='text-align:center; padding:30px 10px;'>
            <p style='font-size:40px;'><b>주문 번호: 105번</b></p>
            <p>직원이 음식을 맛있게 준비하고 있습니다.<br>자리에 앉아서 편하게 기다려주세요! ☕</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 처음 화면으로 돌아가기"):
        st.session_state.cart = []
        st.session_state.selected_item = None
        st.session_state.step = 1
        st.rerun()
