import streamlit as st
import openai
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Set up the page title and description
st.set_page_config(page_title="ThriveX - AI Healing & Self-Mastery", layout="wide")

# Initialize session state
if "mood_history" not in st.session_state:
    st.session_state["mood_history"] = []
if "user_points" not in st.session_state:
    st.session_state["user_points"] = 0
if "user_badges" not in st.session_state:
    st.session_state["user_badges"] = []
if "leaderboard" not in st.session_state:
    st.session_state["leaderboard"] = {}
if "weekly_rewards" not in st.session_state:
    st.session_state["weekly_rewards"] = {}
if "subscription_status" not in st.session_state:
    st.session_state["subscription_status"] = "Free Trial"
if "trial_days_left" not in st.session_state:
    st.session_state["trial_days_left"] = 7
if "months_subscribed" not in st.session_state:
    st.session_state["months_subscribed"] = 0
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "referral_code" not in st.session_state:
    st.session_state["referral_code"] = ""
if "referral_count" not in st.session_state:
    st.session_state["referral_count"] = 0

# Set up Stripe
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"  # Replace with actual API key

# Email Notification Function
SMTP_SERVER = "your.smtp.server.com"  # Replace with actual SMTP server
SMTP_PORT = 587  # Replace with actual port
EMAIL_USERNAME = "your-email@example.com"  # Replace with actual email
EMAIL_PASSWORD = "your-email-password"  # Replace with actual password

def send_email(subject, body, recipient):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = recipient
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, recipient, msg.as_string())
            st.success(f"📧 Email notification sent to {recipient}!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

# ThriveX Branding
st.title("🚀 ThriveX - The Future of Healing & Self-Mastery")
st.write("Your AI-powered transformation hub. Real-time coaching, emotional diagnostics, and immersive healing experiences.")

import random
import string
import pyperclip  # Import pyperclip for copying

# Function to generate a short referral code
def generate_referral_code():
    return "THRIVEX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Generate a referral code if not already created
if "referral_code" not in st.session_state or not st.session_state["referral_code"]:
    st.session_state["referral_code"] = generate_referral_code()

# Display referral code inside a text input (read-only)
st.text_input("Your Referral Code:", value=st.session_state["referral_code"], key="referral_display", disabled=True)

# Single Copy Button
if st.button("Copy Referral Code"):
    pyperclip.copy(st.session_state["referral_code"])  # Copies only the referral code
    st.success(f"Referral code copied: {st.session_state['referral_code']}")

# Track referrals
referred_by = st.text_input("Enter Referral Code (if any):")

if st.button("Apply Referral Code"):
    # Prevent self-referral
    if referred_by == st.session_state["referral_code"]:
        st.error("❌ You cannot use your own referral code.")
    
    # Validate format & store successful referrals
    elif referred_by.startswith("THRIVEX-"):
        st.session_state["referral_count"] += 1
        st.success(f"✅ Referral code applied! You and your referrer both earn a 10% discount.")
    
    else:
        st.error("❌ Invalid referral code. Make sure it's correctly entered.")



# Subscription Model
st.subheader("💳 ThriveX Subscription Plan")
if st.session_state["trial_days_left"] > 0:
    st.write(f"🎉 You are on a **7-day free trial**! Days left: {st.session_state['trial_days_left']}")
else:
    st.write("🔒 Your free trial has ended. Subscribe to continue enjoying ThriveX!")
    plan = st.radio("Choose your plan:", ["Basic - $9.99/month", "Pro - $19.99/month", "Elite - $29.99/month", "Family - $49.99/month (Up to 5 users)", "Group - $99.99/month (Up to 10 users)", "Corporate - $199.99/month (Up to 25 users)"])
    price = int(plan.split("$")[1].split("/")[0])
    
    # Apply automatic loyalty & referral discounts
    if st.session_state["months_subscribed"] >= 6:
        price = price * 0.8  # 20% discount after 6 months
        st.success("🎉 Loyalty Bonus! 20% off for dedicated members.")
    elif st.session_state["months_subscribed"] >= 3:
        price = price * 0.9  # 10% discount after 3 months
        st.success("🎉 Loyalty Discount! 10% off for long-term subscribers.")
    if st.session_state["referral_count"] > 0:
        price = price * 0.9  # 10% discount for referrals
        st.success(f"🎁 Referral Reward! You earned an additional 10% off for referring {st.session_state['referral_count']} friends!")
    
    if st.button("Subscribe Now"):
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": plan
                    },
                    "unit_amount": int(price * 100),
                    "recurring": {"interval": "month"}
                },
                "quantity": 1
            }],
            success_url="https://your-success-url.com",
            cancel_url="https://your-cancel-url.com"
        )
        st.session_state["subscription_status"] = plan
        st.session_state["months_subscribed"] += 1  # Increment subscription count
        st.success(f"✅ Subscription successful! You are now on the {plan} plan.")
        st.markdown(f"[Proceed to Payment]({checkout_session.url})")

# Community Support
st.subheader("🌍 Join the ThriveX Healing Hub")
st.write("Connect with others who are on the same journey. AI-matched support circles coming soon!")

# Call to Action
st.subheader("🚀 Be the First to Experience ThriveX")
st.session_state["user_email"] = st.text_input("Enter your email to join the beta waitlist and receive notifications:")
if st.button("Join Now"):
    st.success("You're on the list! ThriveX Beta launch details will be sent soon.")
