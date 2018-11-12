# Jsonrpc Server and Client

## This directory includes

* `client.py`:
  * The client requests for a graph to be incremented. Before sending the graph to the server, it breaks it down into a dictionary then sends it to the server to be incremented.
* `sever.py`:
  * The server exports the increment method. Receives a dictionary, builds a graph from it, increments it, breaks it down to a dictionary and sends it to the client.
* `request.json`:
  * Contains the json request from the client to the server.
* `node.py`:
  * Which defines a node class.
    * contains a name, list of children, and a count that's initially zero
    * implements a `show(graph)` method recursively prints the nodes within graph
  * An `increment(graph)` method that increments the counts of all nodes within graph.
* `localDemo.py`: which creates a dag of nodes, which it prints, increments, and prints again.

# How to use

* `client.py`:
  * $ python3 client.py
* `server.py`:
  * $ python3 server.py
