Feature: The order service back-end
    As a eCommerce Merchant
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | name           | create_time                        | address                                              | cost_amount | status     | user_id   |
        | Ariana Grande  | 2023-10-18T04:40:35.231701+00:00   | 2671 Wilson Pass Apt. 048 Hessmouth, WI 95473        | 0           | NEW        | 25        |
        | Taylor Swift   | 2023-10-18T04:40:35.231701+00:00   | 9458 Rebecca Valley Lake Williamfort, KY 77271       | 0           | NEW        | 6524      |
        | Kanye West     | 2023-10-18T04:40:35.231701+00:00   | 9458 Rebecca Valley Lake Williamfort, KY 77271       | 0           | NEW        | 2344      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create an Order
    When I visit the "Home Page"
    And I set the "Name" to "Micheal Potter"
    And I set the "Create Time" to "2022-10-18T04:40:35.231701+00:00"
    And I set the "Address" to "2671 Wilson Pass Apt. 048 Hessmouth, WI 95473"
    And I set the "Cost Amount" to "0"
    And I select "NEW" in the "Status" dropdown
    And I set the "User ID" to "1234"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Micheal Potter" in the "Name" field
    And I should see "2022-10-18T04:40:35.231701+00:00" in the "Create Time" field
    And I should see "2671 Wilson Pass Apt. 048 Hessmouth, WI 95473" in the "Address" field
    And I should see "0" in the "Cost Amount" field
    And I should see "NEW" in the "Status" dropdown
    And I should see "1234" in the "User ID" field

