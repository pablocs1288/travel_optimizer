# Travel optimizer

This project comes as result of a challenge I was asked to complete in order to participate in a selection process for a Tech Lead position within a nice financial Startup in São Paulo!

Despite I passed this technical test (yay!), both the company staff and myself agreed I'd be more fittable for other sort of positions, the ones that focus more on a machine learning core and software engineering as well (this is out of scope of this discussion though).

With this, I'm intending to share with you all either the knowledge and the thinking-process that led myself to implement this application the best way I could! Enjoy!

# Challenge description:

A tourist wants to travel around the world minimizing its expenses in plane-tickets regardless the number of stops between an origin and a destination. The application then must deliver the cheaper flight-plan between the chosen origin and destination.

**Example:**

Given the origin **GRU** and the destination **CDG**, all the possible paths between them are:

1. GRU - BRC - SCL - ORL - CDG price **$40**
2. GRU - ORL - CGD price **$64**
3. GRU - CDG price **$75**
4. GRU - SCL - ORL - CDG price **$48**
5. GRU - BRC - CDG price **$45**

The output must be **GRU - BRC - SCL - ORL - CDG**, as its price (**$40**) is the lowest among the others.

**OBS:** For the sake of simplicty, it has been assumed the reverse direction (that is, the origin **CDG** and the destination **GRU** in the last example) maintains the same prices given in the initial price table.


## 1. Execution

The application can be launched through two different ways: 'Local' and 'Image', where the latest intends to ease the setting up by using Docker containers.

### 1.1. Local execution

A shell script is provided to launch the application as follows:

```sh
chmod |x deploy_local.sh
./deploy_local.sh ${INPUT_CSV_PATH}
```

Where the parameter **INPUT_CSV_PATH** represents the csv **path** file (e.x. /usr/data/my_routes.csv) containing the routes and their prices.

The csv format is described below:

|CSV example                          |
|-------------------------------------|
|GRU,BRC,10 |
|BRC,SCL,5  |
|GRU,CDG,75 |
|GRU,SCL,20 |
|GRU,ORL,56 |
|ORL,CDG,5  |
|SCL,ORL,20 |


This mode will only work out if Python 3.6 is installed in the machine (with a correct virtual environment created) along with the next dependencies or python modules:

```sh
pip install --upgrade pip # Optional
pip install PyHamcrest
pip install behave
pip install requests
pip install flask
```

By executing this mode, a shell client will pop up requesting for a route in order to calculate the cheapest path to get at the desired destination as follows **(the booting process will take 4 seconds)**:

```sh
please enter the route (type exit if you want to exit):
```

The input text must follow the next formatting: **ORIGIN-DESTINATION**. If this condition is not fulfilled, an exception is risen.

**At the same time** the bash client starts up, the REST client is launched as well. And when the bash client stops, it performs a POST request to the API in order to shut down the REST client meaning the life-cycle of both clients are attached to each other and the user shouldn't be worried about managing them separately.


### 1.2. Image execution

Similar to the local approach, this mode provides a sh script to launch the shell client and REST client at the same time. It is recommended to use this mode to avoid potential issues of the environment setting up and other tedious configurations as the sh script also manages the image building and the container launching. The only thing to do is to execute the sh script as follows:

```sh
chmod +x deploy_image.sh
./deploy_image.sh ${INPUT_CSV_PATH}
```

The **INPUT_CSV_PATH** parameter is the same one described in the "local execution".

Basically, this mode manages the application's life-cycle the same way the previous approach does, however little differences exist at executing unitary tests with *Behave* (which is going to be explained ahead).

The only requirement this approach needs is to have Docker installed in the machine.


### 1.3. Unitary tests execution

Python offers a widely used BDD framework named *Behave*. Which offers a straightforward language for clients and non-programmers to specify scenarios by using *.fetaure* files. In the other hand, the testing code is in *.py* files and it's written in such a way it's able to receive the inputs and the expected-outputs defined by the scenarios within the *.feature* files.

To run *Behave*, the only thing to do is to move to the project's root directory (where the folder behave must exist as specified by the Behave documentation) and once we are there the *behave* command is invoked as follows:

```sh
cd ${PROJECT_PATH}/
behave feature/
```

**Behave file structure**

```
.
|-- feature
   |-- steps
   |   |-- ".py" files
   |--  ".feature" files
```

#### 1.3.1 Running unitary tests within the container

When the container is launched, the actions performed are just the shell and the REST client launching. As no CI tools are involved to correctly integrate the tests execution to the deployment process yet **(Either for Local and Image execution modes)**, to run tests within the container it's just needed to run the container on *interactive mode* as follows:

```sh
docker run \
    -v=${BASE_PATH}/src/:/usr/web_app/ \
    -v=${BASE_PATH}/database/:/usr/database \
    -p 5000:5000 \
    -e CSV_PATH=${CSV_PATH} \
    -it shortest_path bash
```

**OBS:** At the bottom of the *deploy_image.sh* file, the command above is commented, therefore in order to launch the interactive mode and run the tests is necessary to uncomment this command and to comment the other one.

```sh
# Launch shell and REST client
#docker run \
#    -v=${BASE_PATH}/src/:/usr/web_app/ \
#    -v=${BASE_PATH}/database/:/usr/database \
#    -p 5000:5000 \
#    -e CSV_PATH=${CSV_PATH} \
#    -ti shortest_path

# Interactive mode to execute unitary tests
docker run \
    -v=${BASE_PATH}/src/:/usr/web_app/ \
    -v=${BASE_PATH}/database/:/usr/database \
    -p 5000:5000 \
    -e CSV_PATH=${CSV_PATH} \
    -it shortest_path bash
```

Once the container is up, a bash session of the container is started and now we can perform commands as we were in our local machine.

```sh
behave feature/
```

## 2. File structure

```
.
|-- database
|   |-- routes.csv
|-- src
|   |-- app                         (flask file structure definition)
|   |   |-- __init__.py
|   |   |-- routes.py
|   |-- csv_dao
|   |   |-- persistance_graph.py
|   |-- feature                     (Unitary tests - Behave file structure definition)
|   |   |   |-- steps
|   |   |   |   |-- graph.py
|   |   |   |   |-- persistance.py
|   |   |   |-- graph.feature
|   |   |   |-- persistance.feature
|   |-- services
|   |   |-- graph_operations.py
|   |-- bash_entrypoint.py
|   |-- flask_instance.py           (flask file structure definition)
|-- deploy_image.sh
|-- deploy_local.sh
|-- Dockerfile
|-- Readme.md
|-- launcher.sh
|-- requirements.txt
```

## 2. Solution description

### 2.1. Searching the cheapest route algorithm:

The routes are easily described as a directed-graph where either an origin and destination are nodes, and the price is a weighted-edge between them. Therefore, the well-known Dijkstra's algorithm is used for finding out the shortest path (in this case, the lower price) between two locations or nodes.

As the Dijsktra's algorithm is one of the most used algorithms in this sort of problems, several implementations could be found throughout the Internet, thus, for the sake of agility the choosen implementation was based on [Maria Boldyreva's code](https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc).

This implementation uses **priority queue** in order to make the algorithm even faster (*O(n.logn)* compared with *O(nˆ2)* if it is not used).

**Considerations**

As no further details are given in the description of the problem and from a business perspective, it makes more sense to work with a directed graph. It means the way-back of an edge between two places has different price.

```
PSO-BOG != BOG-PSO
```

If what is required is to work with non-directed graphs **(e.x. PSO-BOG == BOG-PSO)**, an optiniol approach without messing with the code, is to save the way-back edge with the same weight (price):

```
PSO,BOG,50.0
BOG,PSO,50.0
```


### 2.2. Application Design:

The intended design is based on a monolithic approach with model, view and controller layers (MVC) reaching a fair decoupling. Some of the S.O.L.I.D principles like **Single responsibility principle** and **Dependency inversion principle** were considered as the MVC architecture allows a straightforward implementation of them. Other principles were not considered such as **Open/closed principle** as no interfaces or inheritances were used (Python is tricky and verbose in this matter), **Liskov substitution principle** (due to the same reasons) and the **Interface segregation principle** (due to the same reasons).

These decisions where based on the intent of being nice to the other programmers that will see (and maintain) this code as they are good coding practices and stand for a common language for the coders.


## 2.3. API description

As required two endpoints are provided to first, calculate the cheapest path given an origin and a destination, and  second, to register a new route (or edge) within the graph (csv file).

#### 2.4. Register an edge

```bash
http://{hostdomain}:500/register/{origin}/{dest}/{price} 
```

- **METHOD:** 
        - GET
- **PARAMTERS:**
        - origin: origin destination
        - dest: local of detination 
        - price: the cost (or edge`s weight between the origin and destion)
- **RETURNS:**
        - A text pointing out success if the reguster was saved correctly. A text pointing out an error otherwise.

#### 2.5. Register an edge

```bash
http://{hostdomain}:500/bestroute/{origin}/{dest}
```

- **METHOD:** 
        - GET
- **PARAMTERS:**
        - origin: origin destination
        - dest: local of detination 
- **RETURNS:**
        - The cheapest ath between both locations.