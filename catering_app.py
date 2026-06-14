import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import os
from twilio.rest import Client

# ─────────────────────────────────────────────
#  CONFIG & STYLING
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Jade's Cuisine",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FDFAF6;
        color: #1A1A1A;
    }
    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        color: #B5451B;
        margin-bottom: 0;
    }
    .brand-sub {
        font-size: 0.95rem;
        color: #888;
        margin-top: 0;
        letter-spacing: 0.05em;
    }
    .section-label {
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #B5451B;
        margin-bottom: 0.3rem;
    }
    .quote-box {
        background: #fff;
        border-left: 4px solid #B5451B;
        padding: 1.5rem 2rem;
        border-radius: 4px;
        margin-top: 1rem;
    }
    .quote-total {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #B5451B;
    }
    .urgent-badge {
        background: #FEE2E2;
        color: #B91C1C;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .soon-badge {
        background: #FEF3C7;
        color: #92400E;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .ok-badge {
        background: #D1FAE5;
        color: #065F46;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .divider {
        border: none;
        border-top: 1px solid #E5E0D8;
        margin: 1.5rem 0;
    }
    div[data-testid="stButton"] > button {
        background-color: #B5451B;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 2rem;
        font-weight: 500;
        font-size: 0.95rem;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #8F3515;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TWILIO WHATSAPP NOTIFICATION
# ─────────────────────────────────────────────
TWILIO_SID = st.secrets["TWILIO_SID"]
TWILIO_TOKEN = st.secrets["TWILIO_TOKEN"]
TWILIO_FROM = "whatsapp:+14155238886"
NOTIFY_NUMBER = st.secrets["NOTIFY_NUMBER"]

def send_whatsapp_notification(order):
    try:
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
Booking Ref: {order['id']}"""

        client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=NOTIFY_NUMBER
        )
    except Exception as e:
        pass


# ─────────────────────────────────────────────
#  DATA STORAGE
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


# ─────────────────────────────────────────────
#  PRICING LOGIC
# ─────────────────────────────────────────────
PRICING = {
    "Wedding":          5000,
    "Birthday Party":   3500,
    "Corporate Event":  6000,
    "Burial/Funeral":   2500,
}

def calculate_price(event_type, guests):
    base = PRICING[event_type]
    subtotal = base * guests
    if guests >= 100:
        discount = 0.10
    elif guests >= 50:
        discount = 0.05
    else:
        discount = 0.0
    discount_amount = subtotal * discount
    total = subtotal - discount_amount
    return subtotal, discount, discount_amount, total

def urgency(event_date_str):
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    days_left = (event_date - date.today()).days
    if days_left <= 3:
        return "urgent", days_left
    elif days_left <= 7:
        return "soon", days_left
    else:
        return "ok", days_left


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
col_logo, col_nav = st.columns([3, 2])
with col_logo:
    st.markdown('<p class="brand-title">🍽️ Jade\'s Cuisine</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">PREMIUM CATERING SERVICES · NIGERIA</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────
page = st.radio(
    "",
    ["📋 Place an Order", "💰 Get a Quote", "📊 Admin Dashboard"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  PAGE 1 — PLACE AN ORDER
# ═════════════════════════════════════════════
if page == "📋 Place an Order":

    st.markdown('<p class="section-label">New Booking</p>', unsafe_allow_html=True)
    st.markdown("### Tell us about your event")
    st.write("Fill in the details below and we'll get back to you with a confirmation.")

    with st.form("order_form"):
        col1, col2 = st.columns(2)

        with col1:
            client_name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *")
            email = st.text_input("Email Address (optional)")

        with col2:
            event_type = st.selectbox("Type of Event *", list(PRICING.keys()))
            event_date = st.date_input("Event Date *", min_value=date.today())
            guests = st.number_input("Number of Guests *", min_value=1, max_value=5000, value=50, step=10)

        location = st.text_input("Event Location / Venue *")
        special_requests = st.text_area("Special Requests or Notes", placeholder="e.g. vegetarian options, specific dishes, decorations...")

        submitted = st.form_submit_button("Submit Order")

        if submitted:
            if not client_name or not phone or not location:
                st.error("Please fill in all required fields marked with *")
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

                st.success(f"✅ Order submitted successfully! Your booking reference is *{new_order['id']}*")
                st.markdown(f"""
                <div class="quote-box">
                    <p class="section-label">Order Summary</p>
                    <b>{client_name}</b> — {event_type}<br>
                    📅 {event_date.strftime('%d %B %Y')} &nbsp;|&nbsp; 👥 {guests} guests &nbsp;|&nbsp; 📍 {location}<br><br>
                    <span class="quote-total">₦{total:,.0f}</span>
                    {"<br><small style='color:#888'>Includes " + str(int(discount_rate*100)) + "% loyalty discount</small>" if discount_rate > 0 else ""}
                </div>
                """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  PAGE 2 — GET A QUOTE
# ═════════════════════════════════════════════
elif page == "💰 Get a Quote":

    st.markdown('<p class="section-label">Pricing Calculator</p>', unsafe_allow_html=True)
    st.markdown("### How much will your event cost?")
    st.write("Select your event type and guest count to get an instant price estimate.")

    col1, col2 = st.columns([1, 1])

    with col1:
        q_event = st.selectbox("Event Type", list(PRICING.keys()))
        q_guests = st.number_input("Number of Guests", min_value=1, max_value=5000, value=100, step=10)

        if st.button("Calculate Price"):
            subtotal, discount_rate, discount_amt, total = calculate_price(q_event, q_guests)

            st.markdown(f"""
            <div class="quote-box">
                <p class="section-label">Your Estimate</p>
                <b>{q_event}</b> · {q_guests} guests<br><br>
                Base price: ₦{PRICING[q_event]:,} per head<br>
                Subtotal: ₦{subtotal:,.0f}<br>
                {"Discount (" + str(int(discount_rate*100)) + "%): <span style='color:#065F46'>− ₦" + f"{discount_amt:,.0f}</span><br>" if discount_rate > 0 else ""}
                <hr class="divider">
                <span class="quote-total">Total: ₦{total:,.0f}</span>
                <br><br>
                <small style="color:#888">This is an estimate. Final pricing confirmed after consultation.</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-label">Price Guide</p>', unsafe_allow_html=True)
        price_data = {
            "Event Type": list(PRICING.keys()),
            "Price Per Head": [f"₦{v:,}" for v in PRICING.values()]
        }
        st.table(pd.DataFrame(price_data))
        st.markdown("""
        *Volume Discounts:*
        - 50–99 guests → 5% off
        - 100+ guests → 10% off
        """)


# ═════════════════════════════════════════════
#  PAGE 3 — ADMIN DASHBOARD
# ═════════════════════════════════════════════
elif page == "📊 Admin Dashboard":

    st.markdown('<p class="section-label">Admin View</p>', unsafe_allow_html=True)
    st.markdown("### All Orders")

    password = st.text_input("Enter admin password", type="password")

    if password != "Jade2026":
        st.warning("Enter the correct password to access the dashboard.")
        st.stop()

    orders = load_orders()

    if not orders:
        st.info("No orders yet. Orders placed by clients will appear here.")
    else:
        total_orders = len(orders)
        total_revenue = sum(o["total"] for o in orders)
        upcoming = [o for o in orders if (datetime.strptime(o["event_date"], "%Y-%m-%d").date() - date.today()).days >= 0]
        urgent_orders = [o for o in upcoming if (datetime.strptime(o["event_date"], "%Y-%m-%d").date() - date.today()).days <= 3]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Orders", total_orders)
        m2.metric("Total Revenue", f"₦{total_revenue:,.0f}")
        m3.metric("Upcoming Events", len(upcoming))
        m4.metric("🔴 Urgent (≤3 days)", len(urgent_orders))

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Order List — Sorted by Event Date</p>', unsafe_allow_html=True)

        sorted_orders = sorted(orders, key=lambda x: x["event_date"])

        for o in sorted_orders:
            status, days_left = urgency(o["event_date"])

            if status == "urgent":
                badge = f'<span class="urgent-badge">🔴 In {days_left} day(s) — URGENT</span>'
            elif status == "soon":
                badge = f'<span class="soon-badge">🟡 In {days_left} days</span>'
            else:
                badge = f'<span class="ok-badge">🟢 In {days_left} days</span>'

            with st.expander(f"{o['id']} · {o['client_name']} · {o['event_type']} · {o['event_date']}"):
                st.markdown(f"""
                {badge}
                <br><br>
                <b>Client:</b> {o['client_name']}<br>
                <b>Phone:</b> {o['phone']}<br>
                <b>Email:</b> {o['email'] or '—'}<br>
                <b>Event:</b> {o['event_type']}<br>
                <b>Date:</b> {o['event_date']}<br>
                <b>Guests:</b> {o['guests']}<br>
                <b>Location:</b> {o['location']}<br>
                <b>Special Requests:</b> {o['special_requests'] or '—'}<br><br>
                <b>Subtotal:</b> ₦{o['subtotal']:,.0f}<br>
                {"<b>Discount:</b> " + str(int(o['discount_rate']*100)) + "% (−₦" + f"{o['discount_amount']:,.0f})<br>" if o['discount_rate'] > 0 else ""}
                <b style="font-size:1.1rem">Total: ₦{o['total']:,.0f}</b>
                """, unsafe_allow_html=True)
