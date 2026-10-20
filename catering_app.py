import streamlit as st
import pandas as pd
from datetime import datetime, date
import random
import string
from twilio.rest import Client
import requests

st.set_page_config(page_title="Jade's Cuisine", page_icon="dish", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0D0D0D; color: #F0EBE1; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1rem 2rem 1rem !important; max-width: 480px !important; margin: 0 auto !important; }
.hero { background: linear-gradient(160deg, #1A1208 0%, #0D0D0D 60%); border-bottom: 1px solid #2A2218; padding: 2.5rem 1.5rem 2rem; text-align: center; margin: 0 -1rem 2rem; }
.hero-badge { display: inline-block; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #C9A84C; border: 1px solid #C9A84C44; padding: 4px 14px; border-radius: 20px; margin-bottom: 1rem; }
.hero-title { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 700; color: #F0EBE1; line-height: 1.1; margin-bottom: 0.4rem; }
.hero-title span { color: #C9A84C; }
.hero-sub { font-size: 0.85rem; color: #888; }
.card { background: #141414; border: 1px solid #222; border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.card-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #C9A84C; margin-bottom: 0.75rem; }
.card-title { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 600; color: #F0EBE1; margin-bottom: 0.5rem; }
.card-sub { font-size: 0.85rem; color: #666; line-height: 1.5; }
.stTextInput input, .stTextArea textarea { background: #1A1A1A !important; border: 1px solid #2A2A2A !important; border-radius: 10px !important; color: #F0EBE1 !important; }
label { color: #AAA !important; font-size: 0.8rem !important; }
div[data-testid="stButton"] > button { width: 100%; background: #C9A84C; color: #0D0D0D; border: none; border-radius: 12px; padding: 0.9rem 2rem; font-weight: 600; font-size: 0.95rem; margin-top: 0.5rem; }
div[data-testid="stButton"] > button:hover { background: #B8933A; }
.quote-result { background: linear-gradient(135deg, #1A1208, #141414); border: 1px solid #C9A84C44; border-radius: 16px; padding: 1.5rem; margin-top: 1rem; }
.quote-amount { font-family: 'Cormorant Garamond', serif; font-size: 2.5rem; font-weight: 700; color: #C9A84C; }
.quote-detail { font-size: 0.8rem; color: #666; line-height: 1.8; }
.success-box { background: #0A1A0A; border: 1px solid #2A5A2A; border-radius: 16px; padding: 1.5rem; margin-top: 1rem; text-align: center; }
