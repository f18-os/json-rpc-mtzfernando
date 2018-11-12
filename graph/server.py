import socket
from bsonrpc import JSONRpc
from bsonrpc import request, service_class
from bsonrpc.framing import (JSONFramingNone)
from node import *

# Class providing functions for the client to use:
@service_class
class ServerServices(object):
    @request
    def increment(self, graph):
        print("Received from client:", graph)
        root_children = []  # For the children of the root
        root = list(graph)[0]  # Get the name of the root

        for child in graph[root]:
            tmp_child = node(child[0], child[1])
            tmp_child.val = child[2]
            root_children.append(tmp_child)

        root = node(root, root_children)  # Generate the graph
        increment(root)  # Increment the graph

        graph = {root.name: []}  # Start the dictionary to send to the client

        # Populate the dictionary with the children
        for child in root.children:
            graph[root.name].append([child.name, child.children, child.val])

        # Append the new value of the root
        graph[root.name].append(root.val)

        print("Sending to client:", graph, "\n")
        return graph  # Send it to the client


# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50001))
ss.listen(10)

while True:
    s, _ = ss.accept()
    # JSONRpc object spawns internal thread to serve the connection.
    JSONRpc(s, ServerServices(), framing_cls=JSONFramingNone)