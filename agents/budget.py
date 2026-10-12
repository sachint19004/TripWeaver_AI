
def budget_agent(
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
):
    """
    Estimate the total trip cost, including outbound and return
    transport, accommodation, food, local travel, and activities.
    """

    prompt = f"""
You are a practical travel budget planning agent for India.

Prepare a realistic estimated budget for this trip.

TRIP DETAILS
- Starting location: {origin}
- Destination: {destination}
- Duration: {days} days
- Number of travelers: {travelers}
- Total available budget for the entire group: ₹{budget:,.0f}
- Preferred transport: {preferred_transport}
- Travel style: {travel_style}
- Interests: {", ".join(interests) if interests else "Not specified"}
- Additional preferences: {additional_notes or "None"}

YOUR TASK

1. Estimate the cost of travelling from the starting location
   to the destination for all travelers.
2. Include both the outbound and return journeys.
3. Respect the preferred transport:
   - If the preference is "Any suitable option", compare practical
     transport options and recommend the best value option.
   - If a specific transport type is selected, prioritize it.
   - Do not recommend a flight for a route where flying is
     impractical or unavailable without additional ground travel.
4. Estimate accommodation for the entire group and duration.
5. Estimate food and drinking water expenses.
6. Estimate local transportation within the destination.
7. Estimate sightseeing, entry fees, and activities.
8. Include a reasonable miscellaneous expense allowance.
9. Calculate the estimated total and compare it with the budget.
10. State whether the trip appears feasible within the budget.
11. If it exceeds the budget, explain the biggest expenses and
    suggest practical ways to reduce costs.

IMPORTANT RULES
- All costs must be in Indian rupees (INR).
- The budget is for the entire group, not per person.
- Clearly distinguish per-person costs from group totals.
- Use realistic estimates rather than artificially low prices.
- Do not claim that prices, fares, schedules, or availability
  have been verified live.
- Do not invent exact departure times or confirmed ticket fares.
- State important assumptions, including accommodation sharing
  and whether meals are included.
- Avoid counting the same expense twice.
- Include outbound and return transport in the overall total.
- If you cannot confidently estimate a cost, label it as an
  approximate assumption.
- Keep the response structured and easy to read.

Use this output structure:

1. Recommended Transport
   - Recommended mode and why
   - Alternative modes where useful
   - Estimated round-trip cost for the group
   - Important route assumptions

2. Estimated Budget Breakdown
   - Outbound and return transport
   - Accommodation
   - Food
   - Local transportation
   - Activities and sightseeing
   - Miscellaneous
   - Total estimated cost

3. Budget Feasibility
   - Available budget
   - Estimated total
   - Remaining balance or amount over budget
   - Feasibility assessment

4. Cost-Saving Suggestions

5. Assumptions and Limitations

Be transparent about uncertainty. The output is an estimate,
not a live quote or booking confirmation.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text
