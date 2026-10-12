
from concurrent.futures import ThreadPoolExecutor

from agents.destination import destination_agent
from agents.budget import budget_agent
from agents.itinerary import itinerary_agent


def create_travel_plan(
    client,
    destination,
    days,
    travelers,
    budget,
    pace,
    interests,
    travel_style,
    additional_notes
):
    """Coordinate the agents to generate a complete travel plan."""

    # Run Destination and Budget agents concurrently.
    with ThreadPoolExecutor(max_workers=2) as executor:

        destination_future = executor.submit(
            destination_agent,
            client=client,
            destination=destination,
            interests=interests,
            pace=pace,
            additional_notes=additional_notes
        )

        budget_future = executor.submit(
            budget_agent,
            client=client,
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
            travel_style=travel_style,
            interests=interests,
            additional_notes=additional_notes
        )

        # Wait for both agents to finish and retrieve their results.
        destination_result = destination_future.result()
        budget_result = budget_future.result()

    # Generate the itinerary using both agents' results.
    itinerary_result = itinerary_agent(
        client=client,
        destination=destination,
        days=days,
        travelers=travelers,
        budget=budget,
        pace=pace,
        interests=interests,
        travel_style=travel_style,
        additional_notes=additional_notes,
        destination_recommendations=destination_result,
        budget_assessment=budget_result
    )

    return {
        "destination_recommendations": destination_result,
        "budget_assessment": budget_result,
        "itinerary": itinerary_result
    }
