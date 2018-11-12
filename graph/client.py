import socket
from bsonrpc import JSONRpc
from bsonrpc.framing import (
	JSONFramingNone)
from node import *

children_index = 0
leaf1 = node("leaf1")
leaf2 = node("leaf2")

root = node("root", [leaf1, leaf1, leaf2])

print("Graph before increment")
root.show()

# Cut-the-corners TCP Client:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50001))

rpc = JSONRpc(s,framing_cls=JSONFramingNone)
server = rpc.get_peer_proxy()

# Start the dictionary
root_dict = {root.name: []}

# Populate the dictionary with the children information and with out duplicates
for child in root.children:
    root_dict[root.name].append([child.name, child.children, child.val])

# Call the increment method in the server
result = server.increment(root_dict)

# Start modifying the graph with the information sent from the server
root.val = result['root'][len(result['root']) - 1]

# Modify the children's values
for index in range(len(result['root']) - 1):
    root.children[index].val = result['root'][index][2]

print("Graph after increment")
root.show()

rpc.close() # Closes the socket 's' also