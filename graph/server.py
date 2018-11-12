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
        root_children = []                                                # For the children of the root
        root = list(graph)[0]                                             # Get the name of the root
        root_val = graph[root][len(graph[root]) - 1]                      # Get the value of the root
        del graph[root][len(graph[root]) - 1]                             # Delete the root value

        for child in graph[root]:                                         # Traverse every child in the graph
            if not root_children:                                         # If the graph is empty add the child
                tmp_child = node(child[0], child[1])                      # Create the node
                tmp_child.val = child[2]                                  # Assign its value
                root_children.append(tmp_child)                           # Add it to the list
            else:
                in_list = False                                           # Flag to check if node already on the list
                for index in range(len(root_children)):                   # Check the list to see i already there
                    if child[0] == root_children[index].name:             # If there
                        in_list = True                                    # Set flag
                        root_children.append(root_children[index])        # Append the one already in the list again
                        break
                if not in_list:                                           # If not in the list
                    tmp_child = node(child[0], child[1])                  # Create the node
                    tmp_child.val = child[2]                              # Assign its value
                    root_children.append(tmp_child)                       # Add it to the list

        root = node(root, root_children)                                  # Generate the graph
        root.val = root_val                                               # Assign the value of the root
        increment(root)                                                   # Increment the graph

        graph = {root.name: []}                                           # Start the dictionary to send to the client

        for child in root.children:                                       # Populate the dictionary with the children
            graph[root.name].append([child.name, child.children, child.val])

        graph[root.name].append(root.val)                                 # Append the new value of the root

        print("Sending to client:", graph, "\n")
        return graph                                                      # Send it to the client

# Quick-and-dirty TCP Server:
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 50001))
ss.listen(10)

while True:
    s, _ = ss.accept()
    # JSONRpc object spawns internal thread to serve the connection.
    JSONRpc(s, ServerServices(), framing_cls=JSONFramingNone)