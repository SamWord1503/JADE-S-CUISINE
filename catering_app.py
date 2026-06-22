import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import os
from twilio.rest import Client

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Jade's Cuisine",
    page_icon="🍽️",
    layout="centered"
)

# ─────────────────────────────────────────────
#  MOBILE-FIRST STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0D0D0D;
    color: #F0EBE1;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1rem 2rem 1rem !important; max-width: 480px !important; margin: 0 auto !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(160deg, #1A1208 0%, #0D0D0D 60%);
    border-bottom: 1px solid #2A2218;
    padding: 2.5rem 1.5rem 2rem;
    text-align: center;
    margin: 0 -1rem 2rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #C9A84C;
    border: 1px solid #C9A84C44;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #F0EBE1;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.hero-title span { color: #C9A84C; }
.hero-sub {
    font-size: 0.85rem;
    color: #888;
    letter-spacing: 0.05em;
}

/* ── NAV TABS ── */
.nav-container {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    background: #141414;
    padding: 6px;
    border-radius: 14px;
    border: 1px solid #222;
}
.nav-btn {
    flex: 1;
    text-align: center;
    padding: 10px 6px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    color: #666;
    background: transparent;
    border: none;
}
.nav-btn.active {
    background: #C9A84C;
    color: #0D0D0D;
}

/* ── CARDS ── */
.card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 0.75rem;
}
.card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #F0EBE1;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}
.card-sub {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.5;
}

/* ── FORM INPUTS ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    color: #F0EBE1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 2px #C9A84C22 !important;
}
label { color: #AAA !important; font-size: 0.8rem !important; font-weight: 500 !important; }

/* ── BUTTON ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: #C9A84C;
    color: #0D0D0D;
    border: none;
    border-radius: 12px;
    padding: 0.9rem 2rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
    margin-top: 0.5rem;
    transition: all 0.2s;
}
div[data-testid="stButton"] > button:hover {
    background: #B8933A;
    transform: translateY(-1px);
}

/* ── QUOTE BOX ── */
.quote-result {
    background: linear-gradient(135deg, #1A1208, #141414);
    border: 1px solid #C9A84C44;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.quote-amount {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
    margin: 0.5rem 0;
}
.quote-detail {
    font-size: 0.8rem;
    color: #666;
    line-height: 1.8;
}
.discount-tag {
    display: inline-block;
    background: #C9A84C22;
    color: #C9A84C;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 0.5rem;
}

/* ── SUCCESS BOX ── */
.success-box {
    background: #0A1A0A;
    border: 1px solid #2A5A2A;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    text-align: center;
}
.success-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.success-ref {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    color: #4CAF50;
    margin-bottom: 0.3rem;
}
.success-msg { font-size: 0.82rem; color: #666; }

/* ── PRICE TABLE ── */
.price-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #1E1E1E;
    font-size: 0.88rem;
}
.price-row:last-child { border-bottom: none; }
.price-event { color: #CCC; }
.price-amount { color: #C9A84C; font-weight: 600; }

/* ── DISCOUNT TIERS ── */
.tier-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    font-size: 0.82rem;
    color: #666;
    border-bottom: 1px solid #1A1A1A;
}
.tier-row:last-child { border-bottom: none; }

/* ── METRIC CARDS ── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.metric-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #C9A84C;
}
.metric-label { font-size: 0.72rem; color: #666; margin-top: 2px; }

/* ── ORDER CARD ── */
.order-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
}
.order-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}
.order-ref { font-size: 0.72rem; color: #555; font-weight: 600; letter-spacing: 0.1em; }
.order-name { font-size: 1rem; font-weight: 600; color: #F0EBE1; margin-top: 2px; }
.order-event { font-size: 0.8rem; color: #888; margin-top: 1px; }
.badge-urgent { background: #3A0A0A; color: #FF6B6B; font-size: 0.68rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; border: 1px solid #FF6B6B44; }
.badge-soon { background: #2A1E0A; color: #FFB347; font-size: 0.68rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; border: 1px solid #FFB34744; }
.badge-ok { background: #0A1E0A; color: #69DB7C; font-size: 0.68rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; border: 1px solid #69DB7C44; }
.order-details { font-size: 0.8rem; color: #666; line-height: 1.8; }
.order-total { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: #C9A84C; font-weight: 700; margin-top: 0.5rem; }

/* ── CONTACT & BANK ── */
.contact-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.85rem 0;
    border-bottom: 1px solid #1E1E1E;
    font-size: 0.88rem;
}
.contact-item:last-child { border-bottom: none; }
.contact-icon { font-size: 1.2rem; width: 2rem; text-align: center; }
.contact-label { font-size: 0.68rem; color: #555; text-transform: uppercase; letter-spacing: 0.1em; }
.contact-value { color: #CCC; margin-top: 1px; }

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    font-size: 0.72rem;
    color: #333;
    border-top: 1px solid #1A1A1A;
    margin-top: 2rem;
}

/* ── PASSWORD ── */
.stTextInput input[type="password"] {
    background: #1A1A1A !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    color: #F0EBE1 !important;
}

/* Radio hide */
div[data-testid="stRadio"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TWILIO
# ─────────────────────────────────────────────
def send_whatsapp_notification(order):
    try:
        TWILIO_SID = st.secrets["TWILIO_SID"]
        TWILIO_TOKEN = st.secrets["TWILIO_TOKEN"]
        NOTIFY_NUMBER = st.secrets["NOTIFY_NUMBER"]
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = f"""🍽️ NEW ORDER — Jade's Cuisine

Client: {order['client_name']}
Phone: {order['phone']}
Event: {order['event_type']}
Date: {order['event_date']}
Guests: {order['guests']}
Location: {order['location']}
Special Requests: {order['special_requests'] or 'None'}

Total: ₦{order['total']:,.0f}
Ref: {order['id']}"""
        client.messages.create(body=message, from_="whatsapp:+14155238886", to=NOTIFY_NUMBER)
    except:
        pass


# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
DATA_FILE = "orders.json"

def load_orders():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(DATA_FILE, "w") as f:
        json.dump(orders, f, indent=2)

PRICING = {
    "Wedding": 5000,
    "Birthday Party": 3500,
    "Corporate Event": 6000,
    "Burial/Funeral": 2500,
}

def calculate_price(event_type, guests):
    base = PRICING[event_type]
    subtotal = base * guests
    discount = 0.10 if guests >= 100 else 0.05 if guests >= 50 else 0.0
    discount_amount = subtotal * discount
    return subtotal, discount, discount_amount, subtotal - discount_amount

def urgency(event_date_str):
    days_left = (datetime.strptime(event_date_str, "%Y-%m-%d").date() - date.today()).days
    if days_left <= 3:
        return "urgent", days_left
    elif days_left <= 7:
        return "soon", days_left
    return "ok", days_left


# ─────────────────────────────────────────────
#  SESSION STATE FOR NAV
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "order"


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Premium Catering · Ibadan, Oyo State</div>
    <div class="hero-title">Jade's<br><span>Cuisine</span></div>
    <div class="hero-sub">Exceptional food. Unforgettable events.</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  NAV BUTTONS
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 Book Event", key="nav_order"):
        st.session_state.page = "order"
with col2:
    if st.button("💰 Get Quote", key="nav_quote"):
        st.session_state.page = "quote"
with col3:
    if st.button("📊 Dashboard", key="nav_admin"):
        st.session_state.page = "admin"

st.markdown("---")
page = st.session_state.page


# ═════════════════════════════════════════════
#  PAGE 1 — BOOK EVENT
# ═════════════════════════════════════════════
if page == "order":
    st.markdown("""
    <div class="card">
        <div class="card-label">New Booking</div>
        <div class="card-title">Tell us about your event</div>
        <div class="card-sub">Fill in your details below and we'll confirm your booking.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("order_form"):
        client_name = st.text_input("Full Name *")
        phone = st.text_input("Phone Number *")
        email = st.text_input("Email Address (optional)")
        event_type = st.selectbox("Type of Event *", list(PRICING.keys()))
        event_date = st.date_input("Event Date *", min_value=date.today())
        guests = st.number_input("Number of Guests *", min_value=1, max_value=5000, value=50, step=10)
        location = st.text_input("Event Venue / Location *")
        special_requests = st.text_area("Special Requests", placeholder="e.g. Jollof rice, Fried rice, Chicken, Beef...")
        submitted = st.form_submit_button("Submit Booking")

        if submitted:
            if not client_name or not phone or not location:
                st.error("Please fill in all required fields.")
            else:
                subtotal, discount_rate, discount_amt, total = calculate_price(event_type, guests)
                new_order = {
                    "id": f"ORD{len(load_orders()) + 1:04d}",
                    "client_name": client_name,
                    "phone": phone,
                    "email": email,
                    "event_type": event_type,
                    "event_date": str(event_date),
                    "guests": guests,
                    "location": location,
                    "special_requests": special_requests,
                    "subtotal": subtotal,
                    "discount_rate": discount_rate,
                    "discount_amount": discount_amt,
                    "total": total,
                    "status": "Pending",
                    "booked_on": str(date.today())
                }
                orders = load_orders()
                orders.append(new_order)
                save_orders(orders)
                send_whatsapp_notification(new_order)

                st.markdown(f"""
                <div class="success-box">
                    <div class="success-icon">✅</div>
                    <div class="success-ref">{new_order['id']}</div>
                    <div class="success-msg">Booking received! We'll contact you shortly to confirm.<br><br>
                    <b style="color:#C9A84C">Total: ₦{total:,.0f}</b>
                    {"<br><small style='color:#555'>10% discount applied</small>" if discount_rate == 0.10 else "<br><small style='color:#555'>5% discount applied</small>" if discount_rate == 0.05 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  PAGE 2 — GET QUOTE
# ═════════════════════════════════════════════
elif page == "quote":
    st.markdown("""
    <div class="card">
        <div class="card-label">Pricing Calculator</div>
        <div class="card-title">How much will it cost?</div>
        <div class="card-sub">Get an instant estimate for your event.</div>
    </div>
    """, unsafe_allow_html=True)

    q_event = st.selectbox("Event Type", list(PRICING.keys()))
    q_guests = st.number_input("Number of Guests", min_value=1, max_value=5000, value=100, step=10)

    if st.button("Calculate Price"):
        subtotal, discount_rate, discount_amt, total = calculate_price(q_event, q_guests)
        discount_text = f'<div class="discount-tag">🎉 {int(discount_rate*100)}% volume discount applied — you save ₦{discount_amt:,.0f}</div>' if discount_rate > 0 else ""
        st.markdown(f"""
        <div class="quote-result">
            <div style="font-size:0.72rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;">Your Estimate</div>
            <div class="quote-amount">₦{total:,.0f}</div>
            <div class="quote-detail">
                {q_event} · {q_guests} guests<br>
                ₦{PRICING[q_event]:,} per head
            </div>
            {discount_text}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-label">Price Guide</div>
    """, unsafe_allow_html=True)

    for event, price in PRICING.items():
        st.markdown(f"""
        <div class="price-row">
            <span class="price-event">{event}</span>
            <span class="price-amount">₦{price:,}/head</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <br>
        <div class="card-label">Volume Discounts</div>
        <div class="tier-row"><span>50 – 99 guests</span><span style="color:#C9A84C">5% off</span></div>
        <div class="tier-row"><span>100+ guests</span><span style="color:#C9A84C">10% off</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Contact & Bank
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-label">Contact & Payment</div>
        <div class="contact-item">
            <div class="contact-icon">📞</div>
            <div>
                <div class="contact-label">Phone / WhatsApp</div>
                <div class="contact-value">09032803609</div>
            </div>
        </div>
        <div class="contact-item">
            <div class="contact-icon">📘</div>
            <div>
                <div class="contact-label">Facebook</div>
                <div class="contact-value">Jade's Cuisine</div>
            </div>
        </div>
        <div class="contact-item">
            <div class="contact-icon">📍</div>
            <div>
                <div class="contact-label">Location</div>
                <div class="contact-value">Ibadan, Oyo State</div>
            </div>
        </div>
        <div class="contact-item">
            <div class="contact-icon">🏦</div>
            <div>
                <div class="contact-label">Bank — Opay</div>
                <div class="contact-value">9032803609</div>
                <div style="font-size:0.78rem;color:#555">Iyiola Samuel Olatunji</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  PAGE 3 — ADMIN DASHBOARD
# ═════════════════════════════════════════════
elif page == "admin":
    st.markdown("""
    <div class="card">
        <div class="card-label">Admin Access</div>
        <div class="card-title">Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("Enter password", type="password", placeholder="Admin password")

    if password != "Jade2026":
        st.warning("Enter the correct password to access the dashboard.")
        st.stop()

    orders = load_orders()

    if not orders:
        st.info("No orders yet.")
    else:
        total_orders = len(orders)
        total_revenue = sum(o["total"] for o in orders)
        upcoming = [o for o in orders if (datetime.strptime(o["event_date"], "%Y-%m-%d").date() - date.today()).days >= 0]
        urgent_count = len([o for o in upcoming if (datetime.strptime(o["event_date"], "%Y-%m-%d").date() - date.today()).days <= 3])

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{total_orders}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">₦{total_revenue/1000:.0f}k</div>
                <div class="metric-label">Total Revenue</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(upcoming)}</div>
                <div class="metric-label">Upcoming</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color:#FF6B6B">{urgent_count}</div>
                <div class="metric-label">Urgent (≤3 days)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.72rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.75rem;">All Orders — Sorted by Date</div>', unsafe_allow_html=True)

        sorted_orders = sorted(orders, key=lambda x: x["event_date"])

        for o in sorted_orders:
            status, days_left = urgency(o["event_date"])
            if status == "urgent":
                badge = f'<span class="badge-urgent">🔴 {days_left}d — URGENT</span>'
            elif status == "soon":
                badge = f'<span class="badge-soon">🟡 In {days_left} days</span>'
            else:
                badge = f'<span class="badge-ok">🟢 In {days_left} days</span>'

            with st.expander(f"{o['id']} · {o['client_name']} · {o['event_date']}"):
                st.markdown(f"""
                <div style="padding:0.5rem 0">
                    {badge}
                    <div class="order-details" style="margin-top:0.75rem">
                        <b style="color:#AAA">Client:</b> {o['client_name']}<br>
                        <b style="color:#AAA">Phone:</b> {o['phone']}<br>
                        <b style="color:#AAA">Email:</b> {o['email'] or '—'}<br>
                        <b style="color:#AAA">Event:</b> {o['event_type']}<br>
                        <b style="color:#AAA">Date:</b> {o['event_date']}<br>
                        <b style="color:#AAA">Guests:</b> {o['guests']}<br>
                        <b style="color:#AAA">Venue:</b> {o['location']}<br>
                        <b style="color:#AAA">Requests:</b> {o['special_requests'] or '—'}
                    </div>
                    <div class="order-total">₦{o['total']:,.0f}</div>
                    {"<div style='font-size:0.72rem;color:#555'>Includes " + str(int(o['discount_rate']*100)) + "% discount</div>" if o['discount_rate'] > 0 else ""}
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🍽️ Jade's Cuisine · Ibadan, Oyo State<br>
    © 2026 All rights reserved
</div>
""", unsafe_allow_html=True)
