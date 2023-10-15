#!/usr/bin/python3
from sys import argv
from multiprocessing import Pool
import time
import argparse
from helpers.tree import * 

def startTree(filename: str, readFrom: str, saveToFile: str, bandwidth: bool) -> Tree:
    """Reads address, prefix, AS from IPtoASMappings and saves in Nodes of Tree

    Opens IPtoASMappings file and loops through every line to read the IP 
    address, prefix, and AS that controls that IP range. 
    ARGS:
        filename: Caida file to read AS/IP pairings from
        readFrom: list of unique tor IPs
        saveToFile: file to save unique ASes to
        bandwidth: whether to calculate and write bandwidth to file

    Returns:
        address of tree with all nodes of address, prefix, AS added
    """
    #convert addresses to binary and stop once prefix runs out
    tree = Tree()

    with open(filename) as f:
        for newNode in f:
            tree.insert(newNode.split())

    print("Tree finished, moving to searchForAS")
    searchForAS(tree, readFrom, saveToFile, bandwidth)
    return #tree, readFrom, saveToFile]

def searchForAS(tree: Tree, readFrom: str, saveToFile: str, bandwidth: bool):
    """Finds the ASes that the addresses in TorIPListSorted corresponded with.

    Writes to file, listOfAS, the ASes that contained Tor node IP addresses
    from the file, TorIPListSorted. If there is no corresponding AS, 
    it doesn't write anything.

    Args:
        tree: tree contaning the ASes and their IP ranges
        readFrom: list of unique tor IPs
        saveToFile: file to save unique ASes to
        bandwidth: whether to calculate and write bandwidth to file
    """

    try: 
        f = open(readFrom, "r")
    except (OSError, IOError):
        print("Error opening:", readFrom)
        exit(1)

    listOfAS = open(saveToFile, "w+")
    #loop through each file in 
    if bandwidth:
        for l in f:
            lsplit = l.split(" ")
            n = tree.search(lsplit[0])
            if n != None: #found AS for ip
                listOfAS.write(n.AS)
                listOfAS.write(" " + lsplit[1])
            else: #no AS was found
                pass
    else:
        for l in f:
            n = tree.search(l)
            if n != None: #found AS for ip
                listOfAS.write(n.AS)
                listOfAS.write("\n")
            else: #no AS was found
                pass
    listOfAS.close()
    f.close()

    saveToFileBandwidth = saveToFile+"_Bandwidth"
    listASBandwidth(tree, readFrom, saveToFile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=int, required=True, nargs = 2)
    parser.add_argument('-e', type=int, default=None, nargs = 2)
    #TODO: fix -b option
    parser.add_argument('-b', type=bool, default=False)
    args = parser.parse_args()  

    startMonth = args.s[0]
    startYear = args.s[1]
    endMonth = startMonth if args.e is None else args.e[0]
    endYear = startYear if args.e is None else args.e[1]
    bandwidth = args.b
    print("Finding bandwidth: ", bandwidth)

    filenames = []

    while ((startYear < endYear ) or (startMonth <= endMonth and startYear == endYear )):
        formattedMonth = str(startMonth)
        filenames.append(
            ["caidaData/caidaData%s-%s" %(startYear, formattedMonth.zfill(2)),
            "data/formatted/torIPLists/torIPListSorted-%s-%s" % (startYear, formattedMonth.zfill(2)),
            "data/formatted/asLists/listOfAS-%s-%s" %(startYear, formattedMonth.zfill(2)),
            bandwidth
            ])

        startMonth += 1
        if (startMonth == 13):
            startYear += 1
            startMonth = 1

    treeInfo = []
    start_time = time.time()
    print("\nStarting processes in sortTree")
    with Pool(processes=8) as pool:
        tree = pool.starmap(startTree, filenames)

    print("sortTree_Parallel finished running. It took: %i s" %(time.time() - start_time))

    return

if __name__ == '__main__':
    main()
