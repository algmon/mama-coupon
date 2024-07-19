describe('Login Page', () => {
  beforeEach(() => {
    // Visit the login page
    cy.visit('http://localhost:9527/#/login'); 
  });

  it('should display the login form', () => {
    // Verify the presence of the login form elements
    cy.get('form[name="loginForm"]').should('be.visible');
    cy.get('input[name="username"]').should('be.visible');
    cy.get('input[name="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
  });

  it('should display an error message for invalid credentials', () => {
    // Enter invalid credentials
    cy.get('input[name="username"]').type('invaliduser');
    cy.get('input[name="password"]').type('wrongpassword');

    // Submit the form
    cy.get('button[type="submit"]').click();

    // Verify the error message
    cy.get('.error-message').should('be.visible').and('contain', 'Invalid credentials');
  });

  it('should successfully log in with valid credentials', () => {
    // Enter valid credentials
    cy.get('input[name="username"]').type('wei'); // Replace with your test user's username
    cy.get('input[name="password"]').type('123456'); // Replace with your test user's password

    // Submit the form
    cy.get('el-button[type="submit"]').click();

    // Verify successful login (e.g., redirect to dashboard or display a welcome message)
    cy.url().should('include', '/dashboard'); // Replace with your expected URL after login
    // OR
    cy.get('.welcome-message').should('be.visible').and('contain', 'Welcome, testuser!'); // Replace with your welcome message selector and text
  });

  // Add more tests for specific scenarios:
  // - Empty username or password fields
  // - Special characters in username or password
  // - Password strength validation
  // - Account lockout after multiple failed attempts
});
