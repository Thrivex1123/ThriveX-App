import streamlit as st
import openai
import stripe
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Set up the page title and description
st.set_page_config(page_title="ThriveX - AI Healing & Self-Mastery", layout="wide")
# Function to analyze user mood and provide a response
def analyze_mood(mood):
    mood_responses = {
        "Happy": "😊 That's great! Keep spreading positivity!",
        "Sad": "😢 I'm here for you. Consider practicing self-care today.",
        "Stressed": "😓 Take a deep breath. Try meditation or a short walk to clear your mind.",
        "Motivated": "🚀 Awesome! Use this energy to achieve your goals.",
        "Tired": "😴 Make sure to get enough rest and recharge yourself."
    }
    return mood_responses.get(mood, "🤖 I'm not sure how to interpret that mood, but I'm here for you!")

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

# Function to generate a short referral code
def generate_referral_code():
    return "THRIVEX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Generate a referral code if not already created
if "referral_code" not in st.session_state or not st.session_state["referral_code"]:
    st.session_state["referral_code"] = generate_referral_code()

# Display referral code inside a text input (read-only, user can copy manually)
st.text_input("Your Referral Code:", value=st.session_state["referral_code"], key="referral_display", disabled=True)

# Show a message prompting users to copy manually
st.markdown("**📋 Copy your referral code manually from the above box.**")

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
import matplotlib.pyplot as plt
import numpy as np

# Add a new section in ThriveX for the comparison
st.subheader("📊 Financial Stress vs. Quality of Life: Therapy Models")

# Create user input for customization
duration = st.slider("Select Therapy Duration (in years)", min_value=1, max_value=10, value=5)

# Generate time progression based on user selection
time = np.linspace(0, duration, 100)

# Define trajectories for traditional therapy
financial_stress_traditional = np.exp(0.3 * time)  # Steep financial stress increase
quality_of_life_traditional = np.log(time + 1) * 5  # Slow increase, then plateau

# Define trajectories for cost-effective therapy
financial_stress_cost_effective = np.exp(-0.05 * time) + 1  # Low and stable
quality_of_life_cost_effective = np.log(time + 1) * 10  # Steady increase

# Create figure and axis
fig, ax1 = plt.subplots(figsize=(8, 5))

# Plot financial stress for both therapy models
ax1.plot(time, financial_stress_traditional, 'r-', label="Financial Stress (Traditional)")
ax1.plot(time, financial_stress_cost_effective, 'g-', label="Financial Stress (Cost-Effective)")
ax1.set_xlabel("Time (Years)")
ax1.set_ylabel("Financial Stress", color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.legend(loc='upper left')

# Create a second y-axis for quality of life
ax2 = ax1.twinx()
ax2.plot(time, quality_of_life_traditional, 'b--', label="Quality of Life (Traditional)")
ax2.plot(time, quality_of_life_cost_effective, 'c--', label="Quality of Life (Cost-Effective)")
ax2.set_ylabel("Quality of Life", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.legend(loc='lower right')

# Add title and grid
plt.title("Comparison of Quality of Life and Financial Stress in Therapy Models")
plt.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)
import streamlit as st
import openai
import random

# Function to generate a daily affirmation
def get_affirmation():
    affirmations = [
        "You are strong and capable of overcoming any obstacle.",
        "You are enough, just as you are.",
        "Every day, you are getting better and stronger.",
        "Your potential is limitless, and you can achieve anything.",
        "You are worthy of love, happiness, and success."
    ]
    return random.choice(affirmations)

import openai

# Set OpenAI API Key (Replace with your actual key)
openai.api_key = "your_openai_api_key_here"

def chat_with_ai(user_input):
    try:
        client = openai.Client()  # Initialize OpenAI Client
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o for better responses
            messages=[{"role": "user", "content": user_input}],
            temperature=0.7
        )

        # Extract AI's response
        ai_reply = response.choices[0].message.content
        return ai_reply

    except Exception as e:
        return f"⚠️ Error communicating with AI: {str(e)}"





# 🎯 Add ThriveX Functionalities
st.title("🚀 ThriveX - AI Healing & Self-Mastery")

# Daily Affirmation
st.subheader("🌟 Daily Affirmation")
affirmation = get_affirmation()
st.write(f"✨ **{affirmation}** ✨")

# Mood Tracking Section
st.subheader("🧠 How Are You Feeling Today?")
mood = st.selectbox("Select your current mood:", ["Happy", "Sad", "Stressed", "Motivated", "Tired"])
if st.button("Analyze Mood"):
    mood_response = analyze_mood(mood)
    st.success(mood_response)

# AI Chat Section
st.subheader("💬 Talk to ThriveX AI")
user_message = st.text_input("Type your message:")
if st.button("Send Message"):
    if user_message:
        ai_response = chat_with_ai(user_message)
        st.write(f"🤖 AI: {ai_response}")
    else:
        st.error("Please type a message first.")

