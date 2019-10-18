from csv_dao.persistance_graph import GraphDAO
from services.graph_operations import GraphOperations
import requests
import time

time.sleep(4)

def shutdown_flask_server():
    r = requests.post('http://localhost:5000/shutdown')
    if r.status_code == 200:
        print('End-points server shutted down correctly')
        return
    print('problem to shut down the End-points server. Veirfy the process id and kill it manually.')

def formatting_output(stages, price):
    out = ''
    for st in stages:
        out += st + ' - '
    out += '>' + str(price)
    out = out.replace('- >','   =>  ')

    return out

def main():
    route = ''
    while route != 'exit':
        route = input('please enter the route (type exit if you want to exit):')    
        try:    
            input_pr = route.split('-')
            origin, dest = input_pr[0].strip(), input_pr[1].strip()

            graph_dao = GraphDAO()
            g_operations = GraphOperations(graph_dao.get_graph())
            stages, price = g_operations.dijkstra(origin, dest)
            print(formatting_output(stages, price))
        except:
            print('Error, Origin or destination does not exist or perhaps a bad formatted input was the cause. Try to type again!')
            continue

    shutdown_flask_server()
    print('Leaving process!')

if __name__ == '__main__':
    main()