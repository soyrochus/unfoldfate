describe('Card Display Test', () => {
    // before(() => {
    //     // Visit the application
    //     cy.visit('http://localhost:8000'); // Adjust the URL if necessary
    // });

    beforeEach(() => {
        // Visit the application before each test
        cy.visit('http://127.0.0.1:8000/'); // Adjust the URL if necessary
    });

    it('should display the title', () => {
        // Check that the title is displayed
        cy.get('h1').should('contain', 'UnfoldFate');
    });

    it('should display 22 cards', () => {
        // Check that there are 22 cards on the screen
        cy.get('#cards-grid .card').should('have.length', 22);
    });

    it('should click on the button New Reading', () => {
        // Click on the New Reading button for a new reading
        cy.contains('button', 'New Reading').click();
        // Check that the cards are down
        cy.get('#cards-grid .card img').each(($img) => {
            cy.wrap($img).should('have.attr', 'src', '/img/rider-waite-tarot_bg.jpg');
        });
    }
    );

    it('should have the correct background image', () => {
        // Check that the card elements contain images
        cy.get('#cards-grid .card').each(($card) => {
            cy.wrap($card).find('img').should('exist');
        });

        // Check that the background image is correct
        cy.get('#cards-grid .card img').each(($img) => {
            cy.wrap($img).should('have.attr', 'src').and('include', '/img/rider-waite-tarot_bg.jpg');
        });
    });
   
    it('should have a title on each card', () => {
        // Click on the first card
        cy.get('#cards-grid .card').first().click();
        // Check that the card title is displayed
        cy.get('#card-info').each(($card) => {
            cy.wrap($card).find('h2').should('exist');
        });
    });

    it('should have a description on each card', () => {
        // Check that the card description is displayed
        cy.get('#card-info').each(($card) => {
            cy.wrap($card).find('p').should('exist');
        });
    });

    it('should shuffle the cards when clicking New Reading', () => {
        // Get the initial cards
        let initialCards = [];
        // Get the src attribute of each card
        cy.get('#cards-grid .card img').each(($img, index) => {
            cy.wrap($img).invoke('attr', 'src').then((src) => {
                // Store the src attribute in the initialCards array
                initialCards[index] = src;
            });
        });
        // Click on the New Reading button
        cy.contains('button', 'New Reading').click();
        // Get the shuffled cards
        let shuffledCards = [];
        cy.get('#cards-grid .card img').each(($img, index) => {
            cy.wrap($img).invoke('attr', 'src').then((src) => {
                // Store the src attribute in the shuffledCards array
                shuffledCards[index] = src;
            });
        }).then(() => {
            // Check that the initial cards are not equal to the shuffled cards
            expect(initialCards).not.to.deep.equal(shuffledCards);
        });
    });


    it('should receive a valid response from the server', () => {
        // Intercept the POST request to /new-reading
        cy.intercept('POST', '/new-reading').as('newReading');
        // Click on the New Reading button
        cy.contains('button', 'New Reading').click();
        // Wait for the response
        cy.wait('@newReading', { timeout: 10000 }).its('response.statusCode').should('eq', 200);

    });
   
   
});