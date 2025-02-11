"""
UnfoldFate - A Tarot Reading Application using NiceGUI.

This version uses a YAML file with the following structure:

back_ground:
  - image_filename: /img/rider-waite-tarot_bg.jpg
major_arcana:
  - name: The Fool
    description: Beginnings, innocence, spontaneity, a free spirit.
    image_filename: /img/major_arcana_fool.png
  ...
"""

import random
import yaml
from dataclasses import dataclass
from typing import List, Protocol, Optional

from nicegui import ui, app

# ----------------------------------------------------------------------
# 1. Domain Layer: Card and Session Definitions
# ----------------------------------------------------------------------

@dataclass
class Card:
    """
    Represents a Major Arcana tarot card.

    Attributes:
        name (str): The name of the card (e.g., 'The Fool').
        description (str): A brief text describing the card's meaning.
        image_filename (str): The filename for the card's image.
        revealed (bool): True if the card has been turned face-up; otherwise False.
    """
    name: str
    description: str
    image_filename: str
    revealed: bool = False

class TarotSessionProtocol(Protocol):
    def load_cards_from_yaml(self, yaml_path: str) -> None: ...
    def refresh(self) -> None: ...
    def select_card(self, card_id: str) -> None: ...
    def get_cards(self) -> List[Card]: ...
    @property
    def background_image(self) -> str: ...

class TarotSession(TarotSessionProtocol):
    def __init__(self, yaml_path: str = 'rider-waite-tarot.yaml') -> None:
        """
        Initialize a new tarot session, loading card data from the specified YAML file.
        """
        self._cards: List[Card] = []
        self._background_image: Optional[str] = None
        self.selected_card: Optional[str] = None
        self.clicks_enabled: bool = True  # New flag
        self.load_cards_from_yaml(yaml_path)
        self.refresh()

    def load_cards_from_yaml(self, yaml_path: str) -> None:
        """
        Loads the background image and card data (Major Arcana) from a YAML file.
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # Extract background image.
            bg_list = data.get('back_ground', [])
            if bg_list and len(bg_list) > 0:
                self._background_image = bg_list[0].get('image_filename', '')
            # Extract major arcana.
            major_arcana = data.get('major_arcana', [])
            for arcana in major_arcana:
                name = arcana.get('name', 'Unknown')
                description = arcana.get('description', '')
                image_filename = arcana.get('image_filename', '')
                self._cards.append(Card(name, description, image_filename))

    def refresh(self) -> None:
        for card in self._cards:
            card.revealed = False
        random.shuffle(self._cards)
        self.selected_card = None
        self.clicks_enabled = True  # Re-enable clicks on refresh

    def select_card(self, card_id: str) -> None:
        self.selected_card = card_id
        self.clicks_enabled = False  # Disable clicks after selection
        for card in self._cards:
            if card.name == card_id:
                card.revealed = True
                break

    def get_cards(self) -> List[Card]:
        return self._cards

    @property
    def background_image(self) -> str:
        """
        Return the file path for the background image of unrevealed cards.
        """
        return self._background_image if self._background_image else ''

# ----------------------------------------------------------------------
# 2. UI/Presentation Layer
# ----------------------------------------------------------------------

# Create a global session instance.
session = TarotSession()

# Create a container with a responsive grid layout.
cards_container = ui.row().classes('grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 p-4')


name_label = ui.label("").style("display: none")
explanation_label = ui.label("").style("display: none")


def render_cards() -> None:
    """
    Render the card grid based on the current state of the session.
    For each card:
      - If the card is unrevealed, display the background image.
      - If revealed, display the card's own image.
    The selected card has its name and explanation rendered below its image.
    """

    cards_container.clear()
    for card in session.get_cards():
        image_src = card.image_filename if card.revealed else session.background_image
        with cards_container:
            with ui.card().classes("p-2 border border-gray-300 rounded-lg"):
                card_image = ui.image(image_src).classes(
                    "w-[150px] h-[230px] object-cover"
                )
                # Only attach click handler if clicks are enabled
                if session.clicks_enabled:
                    card_image.on('click', lambda e, c_id=card.name: card_clicked(c_id))
   

def card_clicked(card_id: str) -> None:
    """
    Handle the event when a card is clicked.
    Reveals only the selected card and shows its information.
    """
    session.select_card(card_id)
    # Find the selected card and update labels
    for card in session.get_cards():
        if card.name == card_id:
            # Update text and style separately
            name_label.set_text(f"Name: {card.name}")
            name_label.style("display: block")
            
            explanation_label.set_text(f"Explanation: {card.description}")
            explanation_label.style("display: block")
            break
    render_cards()

def new_reading() -> None:
    """
    Handle the "New Reading" event to reset the session and re-render the cards.
    """
    session.refresh()
    name_label.style("display: none")
    explanation_label.style("display: none")
    render_cards()
# ----------------------------------------------------------------------
# 3. Application Layout and Startup
# ----------------------------------------------------------------------

ui.label("UnfoldFate: Your Tarot Reading").style("font-size: 24px; font-weight: bold; margin: 20px;")
ui.button("New Reading", on_click=new_reading).style("margin: 10px;")
# Add the image directory as a static resource for the app.
app.add_static_files('/img', 'img')

# Initial render of the cards when the app starts.
render_cards()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(favicon='img/logo.png', title='UnfoldFate: Your Tarot Reading')