from behave   import given, when, then
from hamcrest import assert_that, equal_to

from services.graph_operations import GraphOperations

@given('a graph')
def step_mocj_graph(context):
    mocked_graph = [('PSO','BOG',30),('BOG','MED',30),('MED','SA',20)]
    context.graph = GraphOperations(mocked_graph)



### Testing unixisting inputs scenario ###

@when('a given node does not exist (origin or destination) {origin} and {destination}')
def step_catch_except(context, origin, destination):
    try:
        context.graph.dijkstra(origin, destination)
        context.message="both keys exist"
    except:
        context.message="unextisting key"


@then('the exception message should be {message}')
def step_compara_price(context, message):
    assert_that(message, context.message)


### Testing shortest path ###

@when('the cheapest way between {origin} and {destination}')
def step_get_origin_destination(context, origin, destination):
    context.origin = origin
    context.destination = destination

@then('the output should be {output}')
def step_compare_price(context, output):
    price = str(context.graph.dijkstra(context.origin, context.destination)[1])
    assert_that(output, equal_to(price))