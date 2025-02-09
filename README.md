# UnfoldFate: A Tarot Reading Application

UnfoldFate is a demo application for near 100% generated code by an AI. It is a Tarot reading application built using [NiceGUI](https://nicegui.io/). This project demonstrates the capabilities of the OpenAI 03-mini-high model in generating functional code with minimal human intervention.

## Installation

To install and run the program, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/unfoldfate.git
    cd unfoldfate
    ```

2. Install [uv](https://github.com/uv-org/uv):
    Follow the instructions on the uv GitHub page to install uv.

3. Create a virtual environment and install dependencies using uv:

    ```sh
    uv pip sync
    ```
    This:
    - Reads dependencies from `pyproject.toml`
    - Installs them inside a virtual environment (`.venv/`)
    - Ensures your environment matches the locked dependencies

    To install locked dependencies only (like `poetry install --no-dev`):

    ```sh
    uv pip sync --only-locked
    ```


4. Activate the virtual environment:
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```

5. Run the application:
    ```sh
    python unfold_fate.py
    ```

![UnfoldFata Tarot Spread](unfold_fate.png)

## How It Was Generated

This application was generated using the OpenAI 03-mini-high model. The process took 4 passes to get it right. The prompt history is included in the `prompt_log.txt` file for reference.

## How It Works

- The application displays a grid of Tarot cards.
- When a card is clicked, it reveals the selected card and displays its name and explanation below the grid.
- The click event is disabled after a card is selected.
- Clicking the "New Reading" button resets the session, shuffles the cards, and re-enables the click event.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Copyright
Copyright 2025 Iwan van der Kleijn