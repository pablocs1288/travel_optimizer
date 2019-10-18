from app import app
from flask import request

from csv_dao.persistance_graph import GraphDAO
from services.graph_operations import GraphOperations


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/register/<origin>/<dest>/<price>', methods=['GET'])
def register_node(origin, dest, price):
    row = (origin,
           dest,
           price)
    try:
        GraphDAO().append_node_to_graph(row)
        return "Route registered correctly"
    except:
        return "Probleam at registering new route"
           


@app.route('/bestroute/<origin>/<dest>', methods=['GET'])
def get_best_route(origin, dest):
    try:
        graph_dao = GraphDAO()
        g_operations = GraphOperations(graph_dao.get_graph())
        stages, price = g_operations.dijkstra(origin, dest)

        return formatting_output(stages, price)
    except:
        return "Probleam finding the path. Origin or destination does not exist, please try again"

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


##### Other methods #####

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def formatting_output(stages, price):
    out = ''
    for st in stages:
        out += st + ' - '
    out += '>' + str(price)
    out = out.replace('- >','   =>  ')

    return out