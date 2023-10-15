class Node:
    """Nodes used to store the IP ranges covered by certain ASes.

    Attributes:
        address: IP address
        prefix: Network prefix
        AS: AS controlling that IP range
        left: address of left child node (0)
        right: address of right child node (0)
        isRoot: true if node is root of tree
        Baddress: Saves IP address in binary form
        leftRight: saves address of node in form RLLRLR...
    """
    def __init__(self):
        self.address = None
        self.prefix = None 
        self.AS = None
        self.left = None #next 0
        self.right = None #next 1
        self.isRoot = None
        self.Baddress = None
        self.leftRight = ""
    
    def __str__(self) -> str:
        """Returns formatted string with node's IP address, network prefix, and AS."""
        return("Address: %s/%s, AS: %s" %(self.address, self.prefix, self.AS))
      