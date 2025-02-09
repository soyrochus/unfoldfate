## Original prompt for UnfoldFate

```markdown

I want a NiceGUI application named “UnfoldFate.” It should load a background image and a list of Major Arcana cards from a YAML file called “raider-wite-tarot.yaml.” The YAML has the following structure:

back_ground:
  - image_filename: /img/rider-waite-tarot_bg.jpg
major_arcana:
  - name: The Fool
    description: Beginnings, innocence, spontaneity, a free spirit.
    image_filename: /img/major_arcana_fool.png
  - name: ...
    description: ...
    image_filename: ...
  ...

Requirements:

1. Each card is shown face-down with the background image. Once clicked, it reveals its actual image (e.g., /img/major_arcana_fool.png).
2. Only one card can be clicked per reading. After the user clicks a card, further clicks should be disabled.
3. When a card is revealed, display its name and description in labels below the “New Reading” button.
4. The layout should be a responsive grid with Tailwind utility classes.
5. The code must serve the “/img” directory as static files.
6. The final code must include the entire Python script, which:
   - Creates a TarotSession class that shuffles cards, loads from YAML, and enforces a single-click rule.
   - Renders the cards in a grid with the background image for face-down and each card’s image for face-up.
   - Contains “New Reading” to reset the session and hide the name/description labels.
   - Uses docstrings and typed dataclasses.

Generate the complete Python code in one file, with a docstring at the top, and reference “ui.run()” under a “if __name__ in {‘__main__’, ‘__mp_main__’}” guard. Also include how to import the needed modules and how the code should structure the session with a “clicks_enabled” or similar boolean.

```

