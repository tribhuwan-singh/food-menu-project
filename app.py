"""
Food Order Manager - Streamlit UI (Menu Board layout)
Structure: Live search bar -> Tabs (My Order / Menu Board / Quick Add / Insights)
Run with: streamlit run food_order_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Food Order Manager",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# THEME / CSS (warm food-truck palette)
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #2b1200 0%, #1a0d05 55%, #100702 100%);
        color: #fff3e6;
    }
    h1, h2, h3 { color: #ffd8a8 !important; }

    /* ---- Signboard hero ---- */
    .signboard {
        position: relative;
        background: #201004;
        border: 1px solid #7c3d10;
        border-radius: 16px;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        box-shadow: 0 10px 26px rgba(0,0,0,0.4);
    }
    .signboard .strip {
        height: 6px;
        background: repeating-linear-gradient(90deg, #ea580c 0 24px, #f59e0b 24px 48px);
    }
    .signboard .body {
        display: flex; align-items: center; justify-content: space-between;
        padding: 20px 28px; flex-wrap: wrap; gap: 16px;
    }
    .signboard .left { display: flex; align-items: center; gap: 16px; }
    .signboard .medallion {
        width: 58px; height: 58px; min-width: 58px; border-radius: 50%;
        background: linear-gradient(135deg, #ea580c, #f59e0b);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.7rem; box-shadow: 0 0 0 3px #201004, 0 0 0 5px #7c3d10;
    }
    .signboard .title-block h1 {
        margin: 0; font-size: 1.7rem; letter-spacing: 2px; text-transform: uppercase;
        color: #ffedd5 !important;
    }
    .signboard .title-block .sub {
        margin-top: 4px; font-size: 0.85rem; color: #fb923c;
        display: flex; align-items: center; gap: 8px;
    }
    .signboard .status-chip {
        background: #16a34a22; border: 1px solid #16a34a; color: #4ade80;
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px;
        padding: 2px 10px; border-radius: 20px;
    }
    .signboard .ticket {
        position: relative;
        border-left: 2px dashed #7c3d10;
        padding-left: 20px;
        text-align: right;
        color: #fff3e6;
    }
    .signboard .ticket .n { font-size: 1.8rem; font-weight: 800; color: #fdba74; line-height: 1; }
    .signboard .ticket .l { font-size: 0.7rem; letter-spacing: 1.5px; color: #fb923c; margin-top: 2px; }

    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: #2a1508; border-radius: 10px 10px 0 0; color: #ffd8a8;
        padding: 8px 18px; font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background: #ea580c !important; color: white !important; }

    .receipt-row {
        display: flex; justify-content: space-between; align-items: center;
        background: linear-gradient(160deg, #3a1a08 0%, #201004 100%);
        border: 1px solid #7c3d10; border-left: 4px solid #f59e0b;
        border-radius: 10px; padding: 10px 16px; margin-bottom: 8px;
    }
    .receipt-row .left { display: flex; align-items: center; gap: 12px; }
    .receipt-row .emoji { font-size: 1.4rem; }
    .receipt-row .name { font-weight: 600; color: #fff3e6; }
    .receipt-row .tag { font-size: 0.7rem; color: #fb923c; }

    .menu-card {
        background: linear-gradient(160deg, #3a1a08 0%, #201004 100%);
        border: 1px solid #7c3d10; border-radius: 14px; padding: 16px;
        text-align: center; margin-bottom: 10px; transition: 0.15s ease;
    }
    .menu-card:hover { transform: translateY(-4px); border-color: #f59e0b; }
    .menu-card .emoji { font-size: 2.2rem; }
    .menu-card .name { color: #fff3e6; font-weight: 700; margin: 6px 0 2px 0; }
    .menu-card .price { color: #fb923c; font-size: 0.85rem; }

    .stat-strip {
        display: flex; gap: 14px; margin-bottom: 16px;
    }
    .stat-box {
        flex: 1; background: linear-gradient(160deg, #3a1a08 0%, #201004 100%);
        border: 1px solid #7c3d10; border-radius: 14px; padding: 14px; text-align: center;
    }
    .stat-box .num { font-size: 1.6rem; font-weight: 800; color: #fdba74; }
    .stat-box .label { font-size: 0.75rem; color: #fb923c; letter-spacing: 0.5px; }

    .stButton>button {
        background: linear-gradient(135deg, #ea580c, #f59e0b); color: white; border: none;
        border-radius: 8px; padding: 6px 14px; font-weight: 700; transition: 0.2s ease;
    }
    .stButton>button:hover { box-shadow: 0 0 15px rgba(245, 158, 11, 0.6); transform: translateY(-1px); }

    .footer-note { color: #c2703a; font-size: 0.8rem; text-align: center; margin-top: 24px; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------------
if "order_items" not in st.session_state:
    st.session_state.order_items = ["Burger", "Pizza", "MOMO", "Pasta", "Dosa"]

if "history" not in st.session_state:
    st.session_state.history = []

CATALOG = {
    "Burger":         {"emoji": "🍔", "price": 149, "tag": "Fast Food"},
    "Pizza":          {"emoji": "🍕", "price": 299, "tag": "Fast Food"},
    "MOMO":           {"emoji": "🥟", "price": 99,  "tag": "Street Food"},
    "Pasta":          {"emoji": "🍝", "price": 199, "tag": "Italian"},
    "Dosa":           {"emoji": "🫓", "price": 89,  "tag": "South Indian"},
    "Ramen":          {"emoji": "🍜", "price": 179, "tag": "Japanese"},
    "Sushi":          {"emoji": "🍣", "price": 349, "tag": "Japanese"},
    "Butter Chicken": {"emoji": "🍗", "price": 259, "tag": "North Indian"},
    "Tiramisu":       {"emoji": "🍰", "price": 159, "tag": "Dessert"},
    "Milk Cake":      {"emoji": "🥛", "price": 119, "tag": "Dessert"},
}

def info(name: str) -> dict:
    return CATALOG.get(name, {"emoji": "🍽️", "price": 0, "tag": "Item"})

def log(action: str):
    st.session_state.history.insert(0, action)
    st.session_state.history = st.session_state.history[:6]

def order_total() -> int:
    return sum(info(i)["price"] for i in st.session_state.order_items)

# ----------------------------------------------------------------------------
# HERO + LIVE CART BADGE
# ----------------------------------------------------------------------------
st.markdown(f"""
<div class="signboard">
    <div class="strip"></div>
    <div class="body">
        <div class="left">
            <div class="medallion">🍽️</div>
            <div class="title-block">
                <h1>Food Order Manager</h1>
                <div class="sub">
                    <span class="status-chip">● OPEN NOW</span>
                    <span>Browse the menu board, build your order, track it live.</span>
                </div>
            </div>
        </div>
        <div class="ticket">
            <div class="n">{len(st.session_state.order_items)} items</div>
            <div class="l">ORDER TOTAL · ₹{order_total()}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LIVE SEARCH BAR (replaces the old sidebar "search item" action)
# ----------------------------------------------------------------------------
search_query = st.text_input("🔍 Search the full menu (order or specials)", placeholder="Type a dish name...")
if search_query:
    matches = [name for name in CATALOG if search_query.lower() in name.lower()]
    if matches:
        st.success(f"Found {len(matches)} match(es): {', '.join(matches)}")
    else:
        st.error("Sorry, no dish matches that search.")

st.write("")

# ----------------------------------------------------------------------------
# TABS - main structural change
# ----------------------------------------------------------------------------
tab_order, tab_board, tab_add, tab_insights = st.tabs(
    ["🧾 My Order", "🌟 Menu Board", "➕ Quick Add", "📊 Insights"]
)

# --- TAB 1: MY ORDER (receipt-style rows with per-row remove) ---------------
with tab_order:
    colA, colB = st.columns([3, 1])
    with colA:
        st.subheader("Your current order")
    with colB:
        if st.button("🧹 Clear all", use_container_width=True):
            st.session_state.order_items.clear()
            log("🧹 Cleared the entire order")
            st.rerun()

    if not st.session_state.order_items:
        st.info("Order list is empty. Head to the Menu Board tab to add something 👉")
    else:
        for idx, item in enumerate(st.session_state.order_items):
            meta = info(item)
            r1, r2 = st.columns([5, 1])
            with r1:
                st.markdown(f"""
                <div class="receipt-row">
                    <div class="left">
                        <span class="emoji">{meta['emoji']}</span>
                        <div>
                            <div class="name">{item}</div>
                            <div class="tag">{meta['tag']} · ₹{meta['price']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                if st.button("❌", key=f"rm_{idx}"):
                    st.session_state.order_items.pop(idx)
                    log(f"➖ Removed **{item}**")
                    st.rerun()

        st.markdown(f"### 💰 Total: ₹{order_total()}")

# --- TAB 2: MENU BOARD (clickable grid, add directly from card) ------------
with tab_board:
    st.subheader("Full menu — tap Add on any dish")
    board_names = list(CATALOG.keys())
    cols = st.columns(5)
    for i, name in enumerate(board_names):
        meta = CATALOG[name]
        with cols[i % 5]:
            st.markdown(f"""
            <div class="menu-card">
                <div class="emoji">{meta['emoji']}</div>
                <div class="name">{name}</div>
                <div class="price">₹{meta['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Add", key=f"add_{name}", use_container_width=True):
                st.session_state.order_items.append(name)
                log(f"➕ Added **{name}**")
                st.rerun()

# --- TAB 3: QUICK ADD (old-style dropdown add, kept for fast repeat orders) -
with tab_add:
    st.subheader("Quick add (repeat order shortcut)")
    qty_choice = st.selectbox("Pick a dish", list(CATALOG.keys()))
    qty = st.number_input("Quantity", min_value=1, max_value=10, value=1)
    if st.button("Add to order"):
        for _ in range(qty):
            st.session_state.order_items.append(qty_choice)
        log(f"➕ Added **{qty_choice} × {qty}**")
        st.success(f"Added {qty} × {qty_choice} to your order.")
        st.rerun()

    st.markdown("---")
    st.subheader("🕓 Recent activity")
    if st.session_state.history:
        for h in st.session_state.history:
            st.markdown(f"- {h}")
    else:
        st.caption("No actions yet.")

# --- TAB 4: INSIGHTS (stats strip + chart) ----------------------------------
with tab_insights:
    st.subheader("Order insights")

    items = st.session_state.order_items
    unique_count = len(set(items))
    total_value = order_total()
    avg_price = round(total_value / len(items), 2) if items else 0

    st.markdown(f"""
    <div class="stat-strip">
        <div class="stat-box"><div class="num">{len(items)}</div><div class="label">TOTAL ITEMS</div></div>
        <div class="stat-box"><div class="num">{unique_count}</div><div class="label">UNIQUE DISHES</div></div>
        <div class="stat-box"><div class="num">₹{total_value}</div><div class="label">ORDER VALUE</div></div>
        <div class="stat-box"><div class="num">₹{avg_price}</div><div class="label">AVG PRICE / ITEM</div></div>
    </div>
    """, unsafe_allow_html=True)

    if items:
        freq = pd.Series(items).value_counts().reset_index()
        freq.columns = ["Item", "Count"]

        fig = go.Figure(go.Bar(
            x=freq["Item"], y=freq["Count"],
            marker=dict(
                color=freq["Count"],
                colorscale=[[0, "#c2410c"], [1, "#fbbf24"]],
                line=dict(color="#f59e0b", width=1),
            ),
            text=freq["Count"], textposition="outside",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fff3e6"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(234,88,12,0.15)"),
            margin=dict(t=10, b=10, l=10, r=10), height=350,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add items to your order to see insights here.")

st.markdown('<div class="footer-note">Made with ❤️ using Streamlit — Food Order Manager</div>', unsafe_allow_html=True)