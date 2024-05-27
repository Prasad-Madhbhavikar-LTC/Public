Feature: Validate customer table data integrity

  Background: 
    Given the customer table exists
    And it has the columns customer_id and email

  Scenario: Customer ID is not null and not empty
    Given I have the customer data
    When I check the customer_id field
    Then no customer_id should be null
    And no customer_id should be an empty string

  Scenario: Email is valid when Customer ID is present
    Given I have the customer data with a valid customer_id
    When I check the email field
    Then the email should be valid
    And the email should not be null

  Scenario: Email is unique for each Customer ID
    Given I have the customer data with a valid customer_id
    When I check the email field for uniqueness
    Then each email should be associated with only one customer_id
