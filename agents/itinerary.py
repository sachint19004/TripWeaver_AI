
def itinerary_agent(
    client,
    origin,
    destination,
    days,
    travelers,
    budget,
    preferred_transport,
    pace,
    interests,
    travel_style,
    additional_notes,
    destination_recommendations,
    budget_assessment,
):
    """
    Generate a day-by-day itinerary that accounts for
    intercity travel, arrival, activities, and the return journey.
    """

    prompt = f"""
You are an experienced travel itinerary planner specializing
in practical trips within India.

Create a realistic day-by-day itinerary using the information
and recommendations provided below.

TRIP DETAILS
- Starting location: {origin}
- Destination: {destination}
- Duration: {days} days, including travel days
- Travelers: {travelers}
- Total group budget: ₹{budget:,.0f}
- Preferred transport: {preferred_transport}
- Preferred pace: {pace}
- Travel style: {travel_style}
- Interests: {", ".join(interests) if interests else "Not specified"}
- Additional notes: {additional_notes or "None"}

DESTINATION RECOMMENDATIONS
{destination_recommendations}

BUDGET ASSESSMENT
{budget_assessment}

ITINERARY REQUIREMENTS

1. Plan the journey from {origin} to {destination}.
2. Treat the requested number of days as the total trip duration,
   including outbound and return travel.
3. Consider the recommended transport option from the budget
   assessment when planning travel days.
4. Allow reasonable time for the outbound journey, arrival,
   local transfer, and accommodation check-in.
5. Do not schedule sightseeing during intercity travel time.
6. Do not assume the traveler arrives early in the morning or
   departs late at night unless that is explicitly established.
7. If exact transport schedules are unknown, describe timing
   broadly, such as "morning departure" or "afternoon arrival",
   only where that is a reasonable planning assumption.
8. Plan activities around the traveler's preferred pace:
   - Relaxed: fewer activities and more downtime.
   - Balanced: a reasonable mix of sightseeing and rest.
   - Packed: more activities, while preserving realistic travel time.
9. Prioritize activities that match the traveler's interests.
10. Consider distance between attractions to avoid unnecessary
    backtracking.
11. Include meals and breaks where appropriate.
12. Account for check-in and check-out where relevant.
13. Reserve sufficient time for the return journey to {origin}.
14. Do not schedule a full day of sightseeing on the return day
    if the traveler needs to travel a significant distance.
15. Keep the budget assessment in mind. Prefer activities and
    transport consistent with the available budget.
16. If the trip duration is too short for the route, explain
    the limitation and suggest a practical alternative.
17. Do not invent confirmed transport schedules, ticket bookings,
    opening hours, or live availability.
18. Do not repeat the same activity unnecessarily.

OUTPUT FORMAT

Start with a short route summary containing:
- Starting location and destination
- Recommended transport
- Total trip duration
- Important travel assumptions

Then provide a day-by-day plan.

For each day, include:
- Morning
- Afternoon
- Evening
- Main activities or travel
- Practical notes

Clearly identify:
- Outbound travel
- Arrival and check-in
- Destination sightseeing
- Return travel

Finish with:
- Practical travel tips
- Any assumptions the traveler should verify before departure

Make the itinerary useful, realistic, and easy to follow.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text
