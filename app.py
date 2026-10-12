
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from agents.orchestration import create_travel_plan


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TripWeaver AI",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# 2. API CONFIGURATION
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Cloud secrets fallback
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

if not api_key:
    st.error(
        "Gemini API key not found. Add GEMINI_API_KEY "
        "to your .env file or Streamlit Cloud secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# 3. CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap'
    );

    :root {
        --forest: #10251f;
        --forest-light: #19382e;
        --gold: #d7b878;
        --gold-light: #f0dca8;
        --ivory: #f5f0e6;
        --muted: #c1c5bc;
        --glass: rgba(13, 28, 23, 0.86);
        --border: rgba(215, 184, 120, 0.28);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            linear-gradient(
                115deg,
                rgba(5, 18, 14, 0.94),
                rgba(10, 28, 22, 0.82),
                rgba(8, 20, 17, 0.92)
            ),
            url(
                "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=2200&q=85"
            );
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: var(--ivory);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: var(--ivory) !important;
    }

    h1, .hero-title {
        font-family: 'Playfair Display', serif !important;
    }

    p, label, li {
        color: var(--ivory);
    }

    .brandbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.7rem 0 1.5rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2.5rem;
    }

    .brand-name {
        color: var(--gold-light);
        font-family: 'Playfair Display', serif;
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .brand-caption {
        color: var(--muted);
        font-size: 0.78rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .hero {
        text-align: center;
        padding: 1.5rem 0 2.5rem 0;
    }

    .eyebrow {
        color: var(--gold);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: clamp(2.6rem, 6vw, 4.8rem);
        font-weight: 600;
        line-height: 1.08;
        margin: 0;
        color: var(--ivory);
    }

    .hero-title span {
        color: var(--gold-light);
        font-style: italic;
    }

    .hero-subtitle {
        color: #d1d5cc;
        font-size: 1.03rem;
        max-width: 650px;
        line-height: 1.8;
        margin: 1.2rem auto 0 auto;
    }

    .section-heading {
        color: var(--gold-light);
        font-family: 'Playfair Display', serif;
        font-size: 1.7rem;
        margin: 0 0 0.4rem 0;
    }

    .section-description {
        color: var(--muted);
        font-size: 0.92rem;
        margin-bottom: 1.5rem;
    }

    .glass-panel {
        background: var(--glass);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.6rem;
        margin: 0.6rem 0 1.4rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }

    .agent-card {
        background: rgba(17, 39, 31, 0.88);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .agent-title {
        color: var(--gold-light);
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .result-banner {
        background: rgba(20, 48, 37, 0.9);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 1.2rem 0 1.8rem 0;
    }

    .result-banner h2 {
        color: var(--gold-light) !important;
        font-family: 'Playfair Display', serif;
        margin-top: 0;
    }

    .result-banner p {
        color: #d9ded5;
        margin-bottom: 0;
    }

    /* Form controls */

    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: var(--ivory) !important;
        font-weight: 500;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background: rgba(7, 19, 15, 0.88) !important;
        border: 1px solid rgba(215, 184, 120, 0.35) !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: var(--ivory) !important;
        background: transparent !important;
        -webkit-text-fill-color: var(--ivory) !important;
    }

    div[data-baseweb="select"] * {
        color: var(--ivory) !important;
    }

    div[data-baseweb="select"] svg {
        fill: var(--gold-light) !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: rgba(215, 184, 120, 0.18) !important;
        border: 1px solid var(--border);
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] span {
        color: var(--ivory) !important;
    }

    [data-testid="stForm"] {
        background: rgba(10, 25, 19, 0.9);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.5rem;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(
            135deg,
            #e4ca8c,
            #c7a65f
        ) !important;
        color: #17271e !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        min-height: 3rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background: var(--gold-light) !important;
        transform: translateY(-1px);
    }

    /* Tabs */

    [data-testid="stTabs"] [role="tablist"] {
        gap: 0.5rem;
        border-bottom: 1px solid var(--border);
    }

    [data-testid="stTabs"] button[role="tab"] {
        color: #d1d5cc !important;
        background: transparent !important;
        border-radius: 8px 8px 0 0;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--gold-light) !important;
        border-bottom: 2px solid var(--gold) !important;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--ivory);
        line-height: 1.75;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        text-align: center;
        color: #aeb8ae;
        font-size: 0.8rem;
        padding-top: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border);
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .brandbar {
            gap: 0.5rem;
        }

        .brand-name {
            font-size: 1.3rem;
        }

        .hero {
            padding-top: 0.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 4. HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="brandbar">
        <div class="brand-name">TripWeaver AI</div>
        <div class="brand-caption">Your journey, thoughtfully planned</div>
    </div>

    <div class="hero">
        <div class="eyebrow">Travel planning, reimagined</div>
        <div class="hero-title">
            Find your next<br>
            <span>great escape.</span>
        </div>
        <div class="hero-subtitle">
            A thoughtful travel companion that brings together
            destinations, transport, budgets, and day-by-day
            itineraries around the way you want to travel.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 5. TRIP PREFERENCES FORM
# --------------------------------------------------

st.markdown(
    """
    <div class="section-heading">Design your journey</div>
    <div class="section-description">
        Tell us a little about your trip. We'll build a plan around
        your route, budget, interests, and preferred pace.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("trip_preferences"):

    st.markdown("#### Your route")

    route_col1, route_col2 = st.columns(2)

    with route_col1:
        origin = st.text_input(
            "Starting location",
            value="",
            placeholder="e.g. Bengaluru, Mumbai, Delhi",
        )

    with route_col2:
        destination = st.text_input(
            "Destination",
            value="",
            placeholder="e.g. Coorg, Goa, Ooty",
        )

    preferred_transport = st.selectbox(
        "Preferred transport",
        options=[
            "Any suitable option",
            "Train",
            "Bus",
            "Flight",
            "Car or bike",
        ],
        index=0,
        help=(
            "Choose a transport type, or let TripWeaver AI "
            "recommend a suitable option."
        ),
    )

    st.markdown("---")
    st.markdown("#### Trip details")

    col1, col2, col3 = st.columns(3)

    with col1:
        days = st.number_input(
            "Duration (days)",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
        )

    with col2:
        travelers = st.number_input(
            "Number of travelers",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )

    with col3:
        budget = st.number_input(
            "Total budget (₹)",
            min_value=1000,
            max_value=1000000,
            value=8000,
            step=1000,
        )

    st.markdown("---")
    st.markdown("#### Your travel style")

    col4, col5 = st.columns(2)

    with col4:
        pace = st.selectbox(
            "Preferred pace",
            options=[
                "Relaxed",
                "Balanced",
                "Packed",
            ],
            index=1,
        )

    with col5:
        travel_style = st.selectbox(
            "Travel style",
            options=[
                "Budget",
                "Comfort",
                "Luxury",
                "Adventure",
            ],
            index=0,
        )

    interests = st.multiselect(
        "What are you interested in?",
        options=[
            "Nature",
            "Adventure",
            "Food",
            "Culture",
            "History",
            "Beaches",
            "Shopping",
            "Nightlife",
            "Wildlife",
            "Photography",
            "Spirituality",
        ],
        default=["Nature", "Food"],
    )

    additional_notes = st.text_area(
        "Anything else we should know?",
        placeholder=(
            "e.g. Prefer seafood, avoid long treks, "
            "need vegetarian food, or want scenic places."
        ),
        height=100,
    )

    submitted = st.form_submit_button(
        "Create my travel plan",
        use_container_width=True,
    )


# --------------------------------------------------
# 6. VALIDATION AND PLAN GENERATION
# --------------------------------------------------

if submitted:

    if not origin.strip():
        st.error("Please enter your starting location.")

    elif not destination.strip():
        st.error("Please enter your destination.")

    else:
        try:
            with st.spinner(
                "Weaving your route, budget, and itinerary together..."
            ):
                # These two new arguments must also be supported
                # by agents/orchestration.py and its downstream agents.
                plan = create_travel_plan(
                    client=client,
                    origin=origin.strip(),
                    destination=destination.strip(),
                    preferred_transport=preferred_transport,
                    days=int(days),
                    travelers=int(travelers),
                    budget=float(budget),
                    pace=pace,
                    interests=interests,
                    travel_style=travel_style,
                    additional_notes=additional_notes.strip(),
                )

            st.session_state["tripweaver_plan"] = plan
            st.session_state["tripweaver_inputs"] = {
                "origin": origin.strip(),
                "destination": destination.strip(),
                "preferred_transport": preferred_transport,
                "days": int(days),
                "travelers": int(travelers),
                "budget": float(budget),
                "pace": pace,
                "interests": interests,
                "travel_style": travel_style,
                "additional_notes": additional_notes.strip(),
            }

        except Exception as error:
            st.error(
                "We couldn't create your travel plan. "
                "Please try again in a moment."
            )
            st.caption(
                "Technical details: "
                f"{type(error).__name__}: {error}"
            )


# --------------------------------------------------
# 7. DISPLAY RESULTS
# --------------------------------------------------

if "tripweaver_plan" in st.session_state:

    plan = st.session_state["tripweaver_plan"]
    trip = st.session_state["tripweaver_inputs"]

    st.markdown(
        f"""
        <div class="result-banner">
            <h2>
                {trip["origin"]} to {trip["destination"]}
            </h2>
            <p>
                {trip["days"]} days &nbsp; | &nbsp;
                {trip["travelers"]} traveler(s) &nbsp; | &nbsp;
                {trip["preferred_transport"]} &nbsp; | &nbsp;
                Budget: ₹{trip["budget"]:,.0f}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Destination ideas",
            "Budget overview",
            "Day-by-day itinerary",
            "Your preferences",
        ]
    )

    with tab1:
        st.markdown("### Discover your destination")
        destination_result = plan.get(
            "destination_recommendations",
            "No destination recommendations were returned.",
        )

        if isinstance(destination_result, (dict, list)):
            st.json(destination_result)
        else:
            st.markdown(str(destination_result))

    with tab2:
        st.markdown("### Understand your budget")
        st.caption(
            "Transport and activity costs are AI-generated estimates, "
            "not confirmed live fares or bookings."
        )

        budget_result = plan.get(
            "budget_assessment",
            "No budget assessment was returned.",
        )

        if isinstance(budget_result, (dict, list)):
            st.json(budget_result)
        else:
            st.markdown(str(budget_result))

    with tab3:
        st.markdown("### Your journey, day by day")

        itinerary_result = plan.get(
            "itinerary",
            "No itinerary was returned.",
        )

        if isinstance(itinerary_result, (dict, list)):
            st.json(itinerary_result)
        else:
            st.markdown(str(itinerary_result))

    with tab4:
        st.markdown("### Your trip preferences")

        st.write(f"**Starting location:** {trip['origin']}")
        st.write(f"**Destination:** {trip['destination']}")
        st.write(
            f"**Preferred transport:** {trip['preferred_transport']}"
        )
        st.write(f"**Duration:** {trip['days']} days")
        st.write(f"**Travelers:** {trip['travelers']}")
        st.write(f"**Budget:** ₹{trip['budget']:,.0f}")
        st.write(f"**Pace:** {trip['pace']}")
        st.write(f"**Travel style:** {trip['travel_style']}")
        st.write(
            "**Interests:** "
            + (
                ", ".join(trip["interests"])
                if trip["interests"]
                else "No specific interests selected"
            )
        )

        if trip["additional_notes"]:
            st.write(
                f"**Additional notes:** {trip['additional_notes']}"
            )

    if st.button("Plan another trip", use_container_width=True):
        del st.session_state["tripweaver_plan"]
        del st.session_state["tripweaver_inputs"]
        st.rerun()


# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        TripWeaver AI · Thoughtful journeys, made simpler
    </div>
    """,
    unsafe_allow_html=True,
)
