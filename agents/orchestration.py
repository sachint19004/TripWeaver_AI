
from concurrent.futures import ThreadPoolExecutor

from agents.destination import destination_agent
from agents.budget import budget_agent
from agents.itinerary import itinerary_agent


def create_travel_plan(
    client,
    origin,
    destination,
    preferred_transport,
    days,
    travelers,
    budget,
    pace,
    interests,
    travel_style,
    additional_notes,
):
    """
    Coordinate the travel-planning agents.

    Destination and budget recommendations run concurrently.
    The itinerary agent then uses both results to create
    a practical day-by-day plan.
    """

    with ThreadPoolExecutor(max_workers=2) as executor:

        destination_future = executor.submit(
            destination_agent,
            client,
            destination,
            interests,
            pace,
            additional_notes,
        )

        budget_future = executor.submit(
            budget_agent,
            client,
            origin,
            destination,
            days,
            travelers,
            budget,
            preferred_transport,
            travel_style,
            interests,
            additional_notes,
        )

        destination_recommendations = destination_future.result()
        budget_assessment = budget_future.result()

    itinerary = itinerary_agent(
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
    )

    return {
        "destination_recommendations": destination_recommendations,
        "budget_assessment": budget_assessment,
        "itinerary": itinerary,
    }
