# ✈️ TripWeaver AI --- Personalized Multi-Agent Travel Planner

**Plan smarter trips with AI-powered destination recommendations, budget
assessment, and personalized itineraries.**

TripWeaver AI is a travel-planning application built with Python,
Streamlit, and Google's Gemini API. It uses three specialized AI agents
coordinated by an orchestrator to turn a traveler's preferences into a
structured travel plan.

## ✨ Features

-   **🗺️ Destination Recommendations:** Suggests attractions and
    activities based on the traveler's interests.
-   **💰 Budget Assessment:** Estimates accommodation, local
    transportation, food, and sightseeing expenses.
-   **🗓️ Personalized Itinerary:** Generates a day-by-day schedule with
    morning, afternoon, and evening activities.
-   **🤖 Multi-Agent Architecture:** Separates destination
    recommendations, budget assessment, and itinerary generation.
-   **⚡ Concurrent Execution:** Runs the Destination and Budget agents
    concurrently before generating the itinerary.
-   **🎨 Interactive Interface:** Collects preferences and displays
    results using Streamlit.
-   **🔐 Environment-Based Configuration:** Loads the Gemini API key
    from an environment file.

## 🛠️ Tech Stack

  Technology           Purpose
  -------------------- ----------------------------------------------
  Python               Application logic and agent implementation
  Streamlit            Interactive web interface
  Google Gemini API    AI-powered travel planning
  Google Gen AI SDK    Communication with Gemini models
  ThreadPoolExecutor   Concurrent execution of the first two agents
  python-dotenv        Loading environment variables
  Git and GitHub       Version control and project hosting

## 🏗️ Architecture

The orchestrator runs the Destination and Budget agents concurrently,
then passes both results to the Itinerary Agent.

``` mermaid
flowchart TD
    A[Traveler Preferences] --> B[Streamlit Frontend]
    B --> C[Orchestrator]
    C --> D[Destination Agent]
    C --> E[Budget Agent]
    D --> F[Collect Agent Results]
    E --> F
    F --> G[Itinerary Agent]
    G --> H[Display Travel Plan]
```

### Agents

**Destination Agent --- `agents/destination.py`**

Recommends attractions and activities based on the destination,
interests, travel pace, and additional preferences.

**Budget Agent --- `agents/budget.py`**

Estimates accommodation, transport, food, and sightseeing costs;
compares the estimate with the available budget and suggests savings.

**Itinerary Agent --- `agents/itinerary.py`**

Creates a day-by-day plan using the Destination Agent's recommendations
and the Budget Agent's assessment.

**Orchestrator --- `agents/orchestration.py`**

Coordinates the agents, collects their outputs, and returns the
completed plan to the frontend.

## 📁 Project Structure

``` text
TripWeaver_AI/
├── agents/
│   ├── __init__.py
│   ├── destination.py
│   ├── budget.py
│   ├── itinerary.py
│   └── orchestration.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

-   Python compatible with the project's dependencies
-   A Google AI Studio account and Gemini API key
-   Git

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/TripWeaver_AI.git
cd TripWeaver_AI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

``` bash
python -m venv .venv
```

On Windows:

``` bash
.venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

**Security:** Never commit `.env` or expose your API key in source code,
screenshots, or a public repository.

### 5. Run the application

``` bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually
`http://localhost:8501`.

## ⚙️ How It Works

1.  The traveler enters destination, trip duration, group size, budget,
    pace, interests, travel style, and optional preferences.
2.  The Streamlit frontend validates required inputs.
3.  The orchestrator starts the Destination and Budget agents
    concurrently.
4.  Both agents send prompts to the configured Gemini model and return
    their responses.
5.  The Itinerary Agent uses both outputs to create the day-by-day plan.
6.  The frontend displays the recommendations, budget assessment,
    itinerary, and trip preferences.

## ⚠️ Current Limitations

-   **Estimated prices:** Budget figures are AI-generated estimates, not
    verified live prices.
-   **No live availability checks:** Opening hours, ticket availability,
    accommodation rates, and restaurant availability are not verified in
    real time.
-   **API dependency:** Generation depends on Gemini availability and
    the quota limits of the configured project and model.
-   **Sequential final stage:** The Itinerary Agent waits for the
    Destination and Budget agents to finish.
-   **Testing and error handling:** Automated tests and more
    comprehensive error handling are planned improvements.

Verify important travel details and prices before booking.

## 🗺️ Roadmap

-   [ ] Improve handling of API quota errors and temporary service
    outages.
-   [ ] Add retry logic with exponential backoff for transient errors.
-   [ ] Add automated tests for agents, orchestration, and input
    validation.
-   [ ] Improve structured output validation and consistency between
    agents.
-   [ ] Add saved trips and itinerary export functionality.
-   [ ] Explore live travel information and price integrations.
-   [ ] Improve deployment and production configuration.

## 🎯 Project Goals

TripWeaver AI is a learning and development project focused on applying
LLMs, modular agent design, orchestration, concurrency, API integration,
and frontend development to a practical use case.

The project is being developed incrementally, with an emphasis on
understanding the implementation, improving reliability, and maintaining
clear separation of responsibilities.

## 👨‍💻 Author

**Sachin T**

-   GitHub: [@sachint19004](https://github.com/sachint19004)
-   LinkedIn: [Sachin T](https://www.linkedin.com/in/sachin-taspire19/)

------------------------------------------------------------------------

*Built with Python, Streamlit, and Google Gemini.*
