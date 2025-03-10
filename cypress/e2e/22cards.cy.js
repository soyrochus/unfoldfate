describe('Card Display Test', () => {
    // before(() => {
    //     // Visit the application
    //     cy.visit('http://localhost:8000'); // Adjust the URL if necessary
    // });

    beforeEach(() => {
        // Visit the application before each test
        cy.visit('http://localhost:8000'); // Adjust the URL if necessary
    });

    it('should display 22 cards', () => {
        // Check that there are 22 cards on the screen
        cy.get('#cards-grid .card').should('have.length', 22);
    });

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
});