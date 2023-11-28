Feature: The order service back-end
    As a eCommerce Merchant
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | name           | create_time                        | address                                              | cost_amount | status     | user_id   |
        | Alex Wang      | 2023-10-18T04:40:35.231701+00:00   | 2671 Wilson Pass Apt. 048 Hessmouth, WI 95473        | 0           | NEW        | 25        |
        | Joseph Walker  | 2023-10-18T04:40:35.231701+00:00   | 9458 Rebecca Valley Lake Williamfort, KY 77271       | 0           | NEW        | 6524      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"