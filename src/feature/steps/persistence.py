from behave   import given, when, then
from hamcrest import assert_that, equal_to

from csv_dao.persistance_graph import GraphDAO


@given('a graph file')
def step_given_put_thing_into_blender(context):
    context.graphDao = GraphDAO()
    context.init_len = len(context.graphDao.get_graph())

@when('the origin is {origin}, the destiny is {destination} and the price is {price}')
def step_when_switch_blender_on(context, origin, destination, price):
    context.new_route = (origin, destination, price)
    
@then('the size of the lines must be bigger by one')
def step_output_should(context):
    context.graphDao.append_node_to_graph(context.new_route)
    context.final_len = len(context.graphDao.get_graph())
    assert_that(context.init_len + 1, equal_to(context.final_len))