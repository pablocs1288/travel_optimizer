Feature: Persist a new route

    Scenario: When a new route is registered in the csv file
        Given a graph file
        When the origin is PSO, the destiny is MED and the price is 60
        Then the size of the lines must be bigger by one