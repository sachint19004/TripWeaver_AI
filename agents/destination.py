
def destination_agent(client, destination, interests, pace, additional_notes):
    """Recommend attractions and activities based on trip preferences."""

    prompt = f"""
    You are the Destination Agent for TripWeaver AI.

    Destination: {destination}
    Interests: {", ".join(interests)}
    Travel pace: {pace}
    Additional preferences: {additional_notes or "None provided"}

    Recommend five attractions or activities that suit this traveler.

    For each recommendation, include:
    - Name of the attraction or activity
    - Why it matches the traveler's interests
    - Suggested time to spend there
    - Any useful practical tips

    Do not create a complete day-by-day itinerary.
    Do not invent current opening hours, ticket prices, or availability.
    Clearly identify details that need verification.
    Keep the response concise and readable.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
