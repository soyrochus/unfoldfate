# UnfoldFate: A Tarot Reading Application

UnfoldFate is a demo application for near 100% generated code by and AI. It is a Tarot reading application built using [NiceGUI](https://nicegui.io/). This project demonstrates the capabilities of the OpenAI 03-mini-high model (and equivalent) in generating functional code with minimal human intervention.

## Installation

To install and run the program, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/unfoldfate.git
    cd unfoldfate
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application using `uv`:
    ```sh
    uv unfold_fate.py
    ```

## How It Was Generated

This application was generated using the OpenAI 03-mini-high model. The process took 4 passes to get it right. The prompt history is included in the `prompt_log.txt` file for reference.

## How to Run

1. Ensure you have followed the installation steps above.
2. Run the application using the command:
    ```sh
    uv unfold_fate.py
    ```
3. Open your web browser and navigate to `http://localhost:8080` to access the application.

## How It Works

- The application displays a grid of Tarot cards.
- When a card is clicked, it reveals the selected card and displays its name and explanation below the grid.
- The click event is disabled after a card is selected.
- Clicking the "New Reading" button resets the session, shuffles the cards, and re-enables the click event.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Copyright
Copyright 2025 Iwan van der Kleijn