import streamlit as st
import openai

import stripe
import random
import string
import matplotlib.pyplot as plt
import numpy as np

# Set up the page title
st.set_page_config(page_title="ThriveX - AI Healing & Self-Mastery", layout="wide")

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"  # Replace with actual Stripe key

# Initialize session state variables
if "mood_history" not in st.session_state:
    st.session_state["mood_history"] = []
if "user_points" not in st.session_state:
    st.session_state["user_points"] = 0
if "subscription_status" not in st.session_state:
    st.session_state["subscription_status"] = "Free Trial"
if "trial_days_left" not in st.session_state:
    st.session_state["trial_days_left"] = 7
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "referral_code" not in st.session_state:
    st.session_state["referral_code"] = ""

# Function to generate a referral code
def generate_referral_code():
    return "THRIVEX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Assign a referral code if not already created
if not st.session_state["referral_code"]:
    st.session_state["referral_code"] = generate_referral_code()

# Daily Affirmations
daily_affirmations = [
    "You are enough, just as you are.",
    "Your potential is limitless, and you can achieve anything.",
    "Every day, you are getting better and stronger.",
    "You are worthy of love, happiness, and success."
]
current_affirmation = random.choice(daily_affirmations)

# Function to interact with OpenAI chatbot
def chat_with_ai(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error communicating with AI: {str(e)}"

# Financial Stress vs Quality of Life Chart
def plot_comparison_chart():
    years = np.arange(1, 11)
    traditional_therapy_quality = np.log1p(years) * 20 + 40
    traditional_therapy_stress = np.exp(0.2 * years) * 20
    cost_effective_quality = np.linspace(40, 85, 10)
    cost_effective_stress = np.linspace(40, 20, 10)
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(years, traditional_therapy_quality, label='Traditional - Quality', linestyle='--')
    ax1.plot(years, cost_effective_quality, label='Cost-Effective - Quality', linestyle='-')
    ax2.plot(years, traditional_therapy_stress, label='Traditional - Stress', linestyle='--', color='r')
    ax2.plot(years, cost_effective_stress, label='Cost-Effective - Stress', linestyle='-', color='r')
    ax1.set_xlabel("Years in Therapy")
    ax1.set_ylabel("Quality of Life (Higher is Better)")
    ax2.set_ylabel("Financial Stress (Lower is Better)")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    st.pyplot(fig)

# ThriveX Branding
st.title("🚀 ThriveX - The Future of Healing & Self-Mastery")
st.write("Your AI-powered transformation hub. Real-time coaching, emotional diagnostics, and immersive healing experiences.")

# Referral Program
st.subheader("🎁 Refer & Earn Rewards!")
st.write("Invite friends and earn a **10% discount** on your next month for every successful referral!")
st.text_input("Your Referral Code:", value=st.session_state["referral_code"], disabled=True)

# Subscription Plan
st.subheader("💳 ThriveX Subscription Plan")
if st.session_state["trial_days_left"] > 0:
    st.write(f"🎉 You are on a **7-day free trial**! Days left: {st.session_state['trial_days_left']}")
else:
    plan = st.radio("Choose your plan:", ["Basic - $9.99/month", "Pro - $19.99/month", "Elite - $29.99/month"])
    price = float(plan.split("$")[1].split("/")[0])
    if st.button("Subscribe Now"):
        st.success(f"✅ Subscription successful! You are now on the {plan} plan.")

# Mood Analysis
st.subheader("🧠 How Are You Feeling Today?")
mood = st.selectbox("Select your current mood:", ["Happy", "Sad", "Stressed", "Motivated", "Anxious"])
if st.button("Analyze Mood"):
    mood_response = f"Your mood is: {mood}. Remember, emotions are temporary and self-care is important!"
    st.success(mood_response)

# AI Chatbot
st.subheader("💬 Talk to ThriveX AI")
user_message = st.text_input("Type your message:")
if st.button("Ask AI"):
    ai_response = chat_with_ai(user_message)
    st.write(f"🤖 AI: {ai_response}")

# Daily Affirmation
st.subheader("🌟 Daily Affirmation")
st.write(f"✨ {current_affirmation} ✨")

# Financial Stress vs. Quality of Life Chart
st.subheader("📊 Financial Stress vs. Quality of Life: Therapy Models")
plot_comparison_chart()

# Beta Waitlist
st.subheader("🚀 Be the First to Experience ThriveX")
st.session_state["user_email"] = st.text_input("Enter your email to join the beta waitlist:")
if st.button("Join Now"):
    st.success("You're on the list! ThriveX Beta launch details will be sent soon.")
