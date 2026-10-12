import os
from dotenv import load_dotenv
import streamlit as st
import time
from google import genai
from agents.orchestration import create_travel_plan

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
start_time = time.time()
st.set_page_config(
    page_title="TripWeaver AI",
    page_icon="🧭",
    layout="wide"
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;600;700;800&display=swap');

.stApp {
    background-color: #F5F7F3;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #142F2B, #286458);
    padding: 2.5rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    color: white;
    font-family: 'Manrope', sans-serif;
    font-size: 2.7rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 0.5rem;
}

.hero p {
    color: #DCEBE4;
    font-size: 1.05rem;
}

.eyebrow {
    color: #B5DDC9;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
}

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #E1E8E0;
    border-radius: 18px;
    padding: 1.4rem;
}

.stButton button,
.stFormSubmitButton button {
    background: #1C594D;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #287666;
    color: white;
}

.agent-card {
    background: white;
    border: 1px solid #E1E8E0;
    border-radius: 15px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.8rem;
}

.agent-card h4 {
    color: #1B4940;
    margin: 0 0 0.4rem 0;
}

.agent-card p {
    color: #65736C;
    margin: 0;
    font-size: 0.9rem;
}

/* Main text and headings */
.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #24352F;
}

/* Headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #173F35;
}

/* AI-generated itinerary and other content blocks */
div[data-testid="stMarkdownContainer"] {
    color: #24352F;
}

div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] strong {
    color: #24352F;
}

/* Input fields */
.stApp input,
.stApp textarea,
.stApp div[data-baseweb="select"] {
    color: #24352F;
    background-color: #FFFFFF;
}

/* Placeholder text */
.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #68776F;
    opacity: 1;
}


/* JSON viewer: dark background, light text */
.stApp div[data-testid="stJson"] {
    background-color: #172923 !important;
    border: 1px solid #355348;
    border-radius: 12px;
    padding: 12px;
    color: #F1F5F2 !important;
}

/* JSON content */
.stApp div[data-testid="stJson"] pre,
.stApp div[data-testid="stJson"] code,
.stApp div[data-testid="stJson"] span {
    color: #F1F5F2 !important;
    background-color: transparent !important;
}


/* Captions and secondary text */
.stApp small,
.stApp div[data-testid="stCaptionContainer"] {
    color: #52645B;
}

/* Keep the hero banner text white and mint */
.hero,
.hero h1 {
    color: #FFFFFF;
}

.hero p {
    color: #DCEBE4;
}

.hero .eyebrow {
    color: #B5DDC9;
}

</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ YOUR PERSONAL AI TRAVEL TEAM</div>
    <h1>Make room for wonder.</h1>
    <p>Thoughtful itineraries. Smarter budgets. Trips designed around you.</p>
</div>
""", unsafe_allow_html=True)

# ---------- PAGE LAYOUT ----------
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.subheader("Design your trip")
    st.write("Tell us what a great trip looks like for you.")

    with st.form("trip_preferences"):
        destination = st.text_input(
            "Where do you want to go?",
            placeholder="e.g. Coorg, Goa, Kyoto"
        )

        col1, col2 = st.columns(2)

        with col1:
            days = st.selectbox(
                "Duration",
                [1, 2, 3, 4, 5, 6, 7],
                index=2,
                format_func=lambda x: f"{x} day" if x == 1 else f"{x} days"
            )

            travelers = st.number_input(
                "Number of travelers",
                min_value=1,
                max_value=12,
                value=2
            )

        with col2:
            budget = st.number_input(
                "Total budget (₹)",
                min_value=1000,
                max_value=500000,
                value=8000,
                step=500
            )

            pace = st.selectbox(
                "Travel pace",
                ["Relaxed", "Balanced", "Packed"],
                index=1
            )

        interests = st.multiselect(
            "What interests you?",
            [
                "Nature", "Adventure", "Food", "Culture",
                "Photography", "History", "Shopping",
                "Nightlife", "Family-friendly"
            ],
            default=["Nature", "Food"]
        )

        travel_style = st.radio(
            "Travel style",
            ["Budget", "Comfort", "Luxury"],
            horizontal=True
        )

        additional_notes = st.text_area(
            "Additional preferences (optional)",
            placeholder="e.g. vegetarian food, minimal walking, hidden gems..."
        )

        submitted = st.form_submit_button(
            "✦ Build my itinerary",
            use_container_width=True
        )

with right:
    st.subheader("Meet your planning team")
    st.write("Three specialized agents collaborate to design your trip.")

    st.markdown("""
    <div class="agent-card">
        <h4>🗺️ Destination Agent</h4>
        <p>Finds activities that match your interests and destination.</p>
    </div>

    <div class="agent-card">
        <h4>💰 Budget Agent</h4>
        <p>Estimates expenses and checks your budget constraints.</p>
    </div>

    <div class="agent-card">
        <h4>🗓️ Itinerary Agent</h4>
        <p>Arranges activities into a practical day-by-day plan.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Our orchestrator will coordinate the agents, validate the results, "
        "and return one coherent travel plan."
    )

# ---------- AI TRAVEL PLAN ----------
if submitted:
    if not destination.strip():
        st.error("Please enter a destination.")
    elif not interests:
        st.warning("Choose at least one interest.")
    else:
        st.success("Your preferences have been captured!")

        try:
            start_time = time.time()

            with st.spinner("Your AI travel team is collaborating..."):
                results = create_travel_plan(
                    client=client,
                    destination=destination,
                    days=days,
                    travelers=travelers,
                    budget=budget,
                    pace=pace,
                    interests=interests,
                    travel_style=travel_style,
                    additional_notes=additional_notes
                )

            elapsed = time.time() - start_time
            st.caption(
                f"Your travel plan was generated in {elapsed:.2f} seconds."
            )

            st.subheader("🗺️ Destination Recommendations")
            st.markdown(results["destination_recommendations"])

            st.subheader("💰 Budget Assessment")
            st.markdown(results["budget_assessment"])

            st.subheader("🗓️ Your Personalized Itinerary")
            st.markdown(results["itinerary"])

        except Exception as e:
            st.error(f"Could not generate your travel plan: {e}")

        st.subheader("Trip Preferences")
        st.json({
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "budget_inr": budget,
            "pace": pace,
            "interests": interests,
            "travel_style": travel_style,
            "additional_notes": additional_notes
        })

    st.caption("Your trip plan is ready. Prices are estimates, not live quotes.")