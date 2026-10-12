
def budget_agent(
    client,
    destination,
    days,
    travelers,
    budget,
    travel_style,
    interests,
    additional_notes
):
    """Estimate travel expenses and assess budget feasibility."""

    prompt = f"""
    You are the Budget Agent for TripWeaver AI.

    Estimate a realistic trip budget using these details:

    Destination: {destination}
    Duration: {days} days
    Travelers: {travelers}
    Total budget in INR: ₹{budget}
    Travel style: {travel_style}
    Interests: {", ".join(interests)}
    Additional preferences: {additional_notes or "None provided"}

    Your responsibilities:
    1. Estimate accommodation, local transport, food and drinks,
       and sightseeing costs.
    2. Show estimated costs in INR for the entire group.
    3. Calculate the estimated total and remaining budget or shortfall.
    4. Explain whether the budget is realistic.
    5. Suggest practical savings if needed.
    6. State any assumptions, including whether travel to and from
       the destination is excluded.
    7. Treat all prices as estimates, not live quotes.
    8. Do not claim that prices or availability have been verified.

    Use clear headings and a readable breakdown.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
