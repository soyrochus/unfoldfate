const express = require("express");
const path = require("path");
const YAML = require("yamljs");

const app = express();
const PORT = 3000;

// Load YAML file
const tarotData = YAML.load("rider-waite-tarot.yaml");

class TarotSession {
    constructor() {
        this.cards = [...tarotData.major_arcana]; // Copy deck
        this.shuffle();
        this.selectedCard = null;
    }

    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    revealCard(index) {
        if (this.selectedCard !== null) return null; // Only one selection allowed
        this.selectedCard = this.cards[index];
        return this.selectedCard;
    }

    reset() {
        this.selectedCard = null;
        this.shuffle();
    }
}

// Single session for the app
const tarotSession = new TarotSession();

// Set EJS as the view engine
app.use('/img', express.static(path.join(__dirname, 'img')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views2'));
app.use(express.static(path.join(__dirname, "public")));

// Serve main page
app.get("/", (req, res) => {
    res.render("index");
});

// API to get shuffled deck
app.get("/api/tarot", (req, res) => {
    res.json({ cards: tarotSession.cards });
});

// API to reveal a card
app.get("/api/tarot/reveal/:index", (req, res) => {
    const index = parseInt(req.params.index);
    const card = tarotSession.revealCard(index);
    if (card) {
        res.json(card);
    } else {
        res.status(400).json({ error: "Card already selected" });
    }
});

// API to reset session
app.get("/api/tarot/reset", (req, res) => {
    tarotSession.reset();
    res.json({ message: "New reading started" });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
