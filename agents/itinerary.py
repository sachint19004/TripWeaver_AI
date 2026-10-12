
def itinerary_agent(
    client,
    destination,
    days,
    travelers,
    budget,
    pace,
    interests,
    travel_style,
    additional_notes,
    destination_recommendations,
    budget_assessment
):
    """Create a day-by-day itinerary using recommendations and budget guidance."""

    prompt = f"""
    You are the Itinerary Agent for TripWeaver AI.

    Create a practical day-by-day itinerary using the information below.

    TRIP DETAILS
    Destination: {destination}
    Duration: {days} days
    Travelers: {travelers}
    Total budget: ₹{budget}
    Travel pace: {pace}
    Interests: {", ".join(interests)}
    Travel style: {travel_style}
    Additional preferences: {additional_notes or "None provided"}

    DESTINATION AGENT RECOMMENDATIONS
    {destination_recommendations}

    BUDGET AGENT ASSESSMENT
    {budget_assessment}

    REQUIREMENTS
    1. Organize the trip by day, with morning, afternoon, and evening activities.
    2. Prioritize activities recommended by the Destination Agent.
    3. Use the Budget Agent's assessment to guide spending.
    4. Respect the requested travel pace and interests.
    5. Match food recommendations to any dietary preferences.
    6. Flag the plan if the estimated costs exceed the budget.
    7. Do not invent verified opening hours, current prices, or availability.
    8. State assumptions and present prices as estimates.
    9. Finish with practical travel tips.

    Return a readable, well-structured itinerary.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
