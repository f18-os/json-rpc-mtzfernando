import socket
from bsonrpc import JSONRpc
from bsonrpc.framing import (JSONFramingNone)
from node import *

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

root_dict = {root.name: []}                                                     # Start the dictionary

for child in root.children:                                                     # Populate the dictionary with the children information
    root_dict[root.name].append([child.name, child.children, child.val])

root_dict[root.name].append(root.val)                                           # The last index in the list is the value of the root

result = server.increment(root_dict)                                            # Call the increment method in the server

root.val = result['root'][len(result['root']) - 1]                              # Set the new value for the root

for index in range(len(result['root']) - 1):                                    # Modify the children's values
    root.children[index].val = result['root'][index][2]

print("Graph after increment")
root.show()                                                                     # Show the graph after the increment

rpc.close()                                                                     # Closes the socket 's' also