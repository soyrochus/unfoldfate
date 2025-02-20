#!/usr/bin/env node
/**
 * UnfoldFate - A Tarot Card Reading Application using Express.js, EJS, and htmx.
 *
 * This application provides a tarot card reading interface based on a
 * YAML configuration (rider-waite-tarot.yaml) and images in the ./img folder.
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const yaml = require('js-yaml');
const bodyParser = require('body-parser');

// --------------------
// Data Classes Equivalent (using Classes)
// --------------------

class TarotCard {
    constructor({ name, description, image_filename }) {
        this.name = name;
        this.description = description;
        this.image_filename = image_filename;
    }
}

class TarotDeck {
    constructor({ back_ground, major_arcana }) {
        this.back_ground = back_ground;
        this.major_arcana = major_arcana;
    }
}

class TarotSession {
    constructor(configPath) {
        this.configPath = configPath;
        this.deck = null;
        this.cards = [];
        this.clicksEnabled = true;
        this.selectedCard = null;
        this.loadConfig();
        this.shuffleCards();
    }

    loadConfig() {
        const data = yaml.load(fs.readFileSync(this.configPath, 'utf8'));
        this.deck = new TarotDeck(data);
        this.cards = this.deck.major_arcana.map(card => new TarotCard(card));
    }

    shuffleCards() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    resetSession() {
        this.clicksEnabled = true;
        this.selectedCard = null;
        this.shuffleCards();
    }
}

// Create global tarot session
const sessionObj = new TarotSession('rider-waite-tarot.yaml');

// --------------------
// Express Application Setup
// --------------------

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/img', express.static(path.join(__dirname, 'img')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Helper function to get context
const getContext = () => ({
    cards: sessionObj.cards.map((card, index) => [index, card]),
    selectedCard: sessionObj.selectedCard,
    clicksEnabled: sessionObj.clicksEnabled,
    deckBack: sessionObj.deck?.back_ground[0]?.image_filename || ''
});


// --------------------
// Routes
// --------------------

app.get('/', (req, res) => {
    res.render('index', getContext());
});

app.post('/new-reading', (req, res) => {
    sessionObj.resetSession();
    res.render('update_fragment', getContext());
});

app.post('/select_card', (req, res) => {
    if (sessionObj.clicksEnabled) {
        const cardIndex = parseInt(req.body.card_index);
        if (!isNaN(cardIndex) && cardIndex >= 0 && cardIndex < sessionObj.cards.length) {
            sessionObj.selectedCard = sessionObj.cards[cardIndex];
            sessionObj.clicksEnabled = false;
        }
    }
    res.render('update_fragment', getContext());
});

// --------------------
// Start Server
// --------------------

const PORT = 8000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
});