#!/usr/bin/env python3
"""
UnfoldFate - A Tarot Card Reading Application using FastAPI, Jinja2, and htmx.

This single‑file application provides a tarot card reading interface based on a
YAML configuration (rider-waite-tarot.yaml) and images in the ./img folder.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import random
import yaml

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from jinja2 import Environment, DictLoader

# ------------------------------
# Data Classes and Session Logic
# ------------------------------

@dataclass
class TarotCard:
    """Represents a single tarot card with its properties."""
    name: str
    description: str
    image_filename: str

@dataclass
class TarotDeck:
    """Represents the tarot deck configuration."""
    back_ground: List[dict]
    major_arcana: List[dict]

class TarotSession:
    """Manages the state and logic of a tarot reading session."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.deck: Optional[TarotDeck] = None
        self.cards: List[TarotCard] = []
        self.clicks_enabled = True
        self.selected_card: Optional[TarotCard] = None
        self.load_config()
        self.shuffle_cards()
    
    def load_config(self) -> None:
        """Load the deck configuration from YAML file."""
        with open(self.config_path, 'r') as file:
            data = yaml.safe_load(file)
            self.deck = TarotDeck(**data)
            self.cards = [TarotCard(**card) for card in self.deck.major_arcana]
    
    def shuffle_cards(self) -> None:
        """Randomize the order of cards in the deck."""
        random.shuffle(self.cards)
    
    def reset_session(self) -> None:
        """Reset the session state for a new reading."""
        self.clicks_enabled = True
        self.selected_card = None
        self.shuffle_cards()

# Create a single global tarot session (for demo purposes)
session_obj = TarotSession('rider-waite-tarot.yaml')

# ------------------------------
# Jinja2 Templates Setup (Single File)
# ------------------------------

template_dict = {
    "index.html": """
<!DOCTYPE html>
<html>
<head>
    <title>UnfoldFate</title>
    <script src="https://unpkg.com/htmx.org@1.9.3"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
<div class="max-w-6xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4 text-center">UnfoldFate</h1>
    <!-- The New Reading button triggers a POST request; the response updates the grid and info via htmx OOB swap -->
    <button hx-post="/new-reading" hx-swap="none" class="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        New Reading
    </button>
    <div id="cards-grid">
        {% include 'cards_grid.html' %}
    </div>
    <div id="card-info" class="mt-4">
        {% include 'card_info.html' %}
    </div>
</div>
</body>
</html>
""",
    "cards_grid.html": """
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
{% for idx, card in cards %}
    <div class="card">
        <img 
            src="{{ card.image_filename if selected_card and selected_card.name == card.name else deck_back }}" 
            class="object-cover border border-white rounded cursor-pointer" 
            style="width:150px; height:230px; {% if not clicks_enabled %}pointer-events: none;{% endif %}"
            {% if clicks_enabled %}
                hx-post="/select_card" 
                hx-vals='{"card_index": "{{ idx }}"}' 
                hx-swap="none"
            {% endif %}
        >
    </div>
{% endfor %}
</div>
""",
    "card_info.html": """
{% if selected_card %}
<div>
    <h2 class="text-xl font-bold mt-4">{{ selected_card.name }}</h2>
    <p class="text-lg mt-2">{{ selected_card.description }}</p>
</div>
{% else %}
<div></div>
{% endif %}
""",
    "update_fragment.html": """
<!-- These two divs are marked for out-of-band (OOB) swapping -->
<div id="cards-grid" hx-swap-oob="true">
    {% include 'cards_grid.html' %}
</div>
<div id="card-info" hx-swap-oob="true">
    {% include 'card_info.html' %}
</div>
"""
}

env = Environment(loader=DictLoader(template_dict))

def render_template(template_name: str, context: dict) -> HTMLResponse:
    """Render a template from the in‑memory dictionary."""
    template = env.get_template(template_name)
    html_content = template.render(**context)
    return HTMLResponse(content=html_content)

def get_context():
    """Collect context variables for the templates based on the current session state."""
    return {
        "cards": list(enumerate(session_obj.cards)),
        "selected_card": session_obj.selected_card,
        "clicks_enabled": session_obj.clicks_enabled,
        "deck_back": session_obj.deck.back_ground[0]['image_filename'] if session_obj.deck and session_obj.deck.back_ground else ""
    }

# ------------------------------
# FastAPI Application and Endpoints
# ------------------------------

app = FastAPI()

# Mount the static directory for images
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = get_context()
    # Although not used in our templates, passing request in context is common
    context["request"] = request
    return render_template("index.html", context)

@app.post("/new-reading", response_class=HTMLResponse)
async def new_reading():
    # Reset the tarot session and return updated fragments
    session_obj.reset_session()
    context = get_context()
    return render_template("update_fragment.html", context)

@app.post("/select_card", response_class=HTMLResponse)
async def select_card(card_index: int = Form(...)):
    # Only process the selection if clicks are enabled
    if session_obj.clicks_enabled:
        try:
            idx = int(card_index)
            if 0 <= idx < len(session_obj.cards):
                session_obj.selected_card = session_obj.cards[idx]
                session_obj.clicks_enabled = False
        except Exception:
            pass
    context = get_context()
    return render_template("update_fragment.html", context)

# ------------------------------
# Run the Application
# ------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("unfold_fate_server:app", host="0.0.0.0", port=8080, reload=True)
