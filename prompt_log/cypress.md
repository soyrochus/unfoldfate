## QUERY 

You are an expert software developer and test engineer. In a node.js (express, server sid generated) I have created a Tarot spread program . The page consist of a single spread of 22 cards of the Major Arcana. I want to include a cypress test (Javascript)

Which, in turn

verifies that the 22 cards are rendered
verifies that the background image is rendered (/img/rider-waite-tarot_bg.jpg)

Generete the file 22cards.cy.js which I will include in the cypress/e2e directory in the project 


The partial html of the page, the part of the grid which contain the cards, is 

<div id="cards-grid">
        <div class="grid grid-cols-6 gap-2">
    
        <div class="card">
            <img src="/img/rider-waite-tarot_bg.jpg" class="object-cover border border-white rounded cursor-pointer" style="width:150px; height:230px; pointer-events: none;">
        </div>


## REPONSE 
ere's a `22cards.cy.js` Cypress test file that does exactly what you're asking for:

- Verifies that **22 cards** are rendered.
- Verifies that the **background image** (`/img/rider-waite-tarot_bg.jpg`) is used in each card.

---

### ✅ `22cards.cy.js`

```javascript
describe('Tarot Spread Page', () => {
  
  beforeEach(() => {
    // Adjust the URL to match your local/test environment
    cy.visit('http://localhost:3000'); 
  });

  it('renders exactly 22 cards', () => {
    cy.get('#cards-grid .card')
      .should('have.length', 22);
  });

  it('each card has the correct background image', () => {
    cy.get('#cards-grid .card img')
      .each(($img) => {
        cy.wrap($img)
          .should('have.attr', 'src', '/img/rider-waite-tarot_bg.jpg');
      });
  });

});
```

---

### ⚙️ How It Works

1. `cy.visit('http://localhost:3000');`
   - Change the URL if your app runs elsewhere.
2. `cy.get('#cards-grid .card')`
   - Selects all `.card` divs inside the grid.
3. `.should('have.length', 22)`
   - Checks you have exactly **22** cards.
4. `.each(($img) => { ... })`
   - Loops over each image inside a `.card` and asserts that the `src` matches the expected path.

