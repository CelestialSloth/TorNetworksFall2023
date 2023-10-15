from helpers.tree_AS_nodes import * 

class Tree:
    """Organizes nodes into a tree structure.
    
    Attributes:
        root: Saves root of tree which is a Node
        isRoot: True if root
    """
    def __init__(self):
        self.root = Node()
        self.root.isRoot = True
    
    def convertToBinary(self, address:str) -> str:
        """Converts given IP address into it's binary form.
            Args:
                address: string of IP address in dot-decimal notation
            
            Returns:
                binaryAddr: IP address in binary form
        """
        try:
            binaryAddr = ''
            splitAddr = address.split('.')
            for x in splitAddr:
                x = bin(int(x))[2:]
                x = '0'*(8 - len(x)) + x
                binaryAddr += x
        except:
            print("Error in sortTree_Parallel.py with addr: ", address)
            return None
        return binaryAddr
    
    def search(self, ipAddr) -> Node:

        """Searches tree for certain IP Address.

            Can return an exact match (ipAddr = currentNode.address), a possibleNode 
            (if the IP address we are searching for is under a range of addresses), or
            no match (return None).

            Args:
                ipAddr: IP Address we are searching for, in dot-decimal notation

            Returns:
                Node or None: returns node with matching IP address or None
        """
        searchBAddr = self.convertToBinary(ipAddr)
        if (searchBAddr == None):
            print("address not found")
            return None
        
        currentNode = self.root
        possibleNode = None

        for i in searchBAddr:
            if currentNode.isRoot == None and currentNode.address != None:
                p = int(currentNode.prefix)
                if searchBAddr[:-p] == currentNode.Baddress[:-p]:#TODO: if under prefix, make sure it counts
                    possibleNode = currentNode
            if i == '0': #left
                if not currentNode.left:
                    return possibleNode
                currentNode = currentNode.left
            elif i == '1': #right
                if not currentNode.right:
                    return possibleNode
                currentNode = currentNode.right
        if currentNode.address == ipAddr:
            return currentNode
        elif possibleNode != None:
            return possibleNode
        else:
            print("not found")
            return None
    
    def insert(self, newNode):
        """Inserts new node into tree and saves the IP addr, prefix, AS.

        Inserts nodes based on their binary address (0 = left, 1 = right) and saves
        path into leftR using l and r. leftR depends on the length of the prefix
        because it represents a range of IP addresses.

        Args:
            address: IP address 
            prefix: Network prefix
            AS: AS that controls the given IP range
        
        Returns:
            currentNode: newly createdNode with given Args as attributes
        """
        address = newNode[0]
        prefix = newNode[1]
        AS = newNode[2]
        if (len(newNode) > 3):
            bandwidth = newNode[3]

        binaryAddr = self.convertToBinary(address)
        currentNode = self.root
        tempPrefix = int(prefix)
        leftR = ""

        while (tempPrefix > 0): 
            if binaryAddr[0] == '0':
                if not currentNode.left: #create left child if doesn't exist
                    currentNode.left = Node()
                currentNode = currentNode.left #switch to that node
                leftR += "l"
            elif binaryAddr[0] == '1':
                if not currentNode.right: 
                    currentNode.right = Node()
                currentNode = currentNode.right
                leftR += "r"
            tempPrefix -= 1
            binaryAddr = binaryAddr[1:]
            #print(binaryAddr, tempPrefix)

        currentNode.AS = AS
        currentNode.prefix = prefix
        currentNode.address = address
        currentNode.Baddress = self.convertToBinary(address)
        currentNode.leftRight = leftR
        #print(currentNode, self.root, leftR)
        return currentNode #TODO: does it check for duplicates?
