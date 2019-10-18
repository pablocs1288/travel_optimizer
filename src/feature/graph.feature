Feature: graph operations feature

    Scenario: When the node does not exist
        Given a graph
        When a given node does not exist (origin or destination) PSO and NAN
        Then the exception message should be unextisting key

    Scenario: When a destination and an origin is given
        Given a graph
        When the cheapest way between PSO and MED
        Then the output should be 60