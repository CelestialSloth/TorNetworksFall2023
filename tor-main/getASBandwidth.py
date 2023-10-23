#!/usr/bin/python3
from os import listdir
from os.path import isfile, join



def main():
    mypath = "data/formatted/asLists/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in files:
        if (f.split("-", 1)[0] == "sortedListOfAS"):
            listASBandwidth(f)

def listASBandwidth(readFrom):
    """Finds the ASes that the addresses in TorIPListSorted corresponded with. 
    Sums and writes bandwidth to file. 

    Args:
        tree: tree contaning the ASes and their IP ranges
        readFrom: list of ASes and Bandwidths
        saveToFile: file to save AS Bandwidths to
    """
    year = readFrom.split("-")[1]
    month = readFrom.split("-")[2]

    writeTo= "data/formatted/asLists/" + "bandwidthPerAS" + '.csv'
    writeTo2= "data/formatted/asLists/" + "bandwidthPerRelay" + ".csv"

    try: 
        f = open("data/formatted/asLists/" + readFrom, "r")
    except(OSError, IOError):
        print("Error opening:", readFrom)
        exit(1)

    listOfASBandwidth = open(writeTo, "a+")
    listOfASBandwidthPerRelay = open(writeTo2, "a+")

    lastAS = "0"
    sumBand = 0
    numRelay = 0
    for l in f:
        numRelay += 1
        lsplit = l.split(" ")
        currentBand = lsplit[1] 
        currentAS = lsplit[0]
        if ((lastAS != currentAS) & (lastAS != "0")):
            listOfASBandwidth.write(year + ',' + month + ',' + lastAS + ',' + str(numRelay) + ',')
            listOfASBandwidth.write(" " + str(sumBand)+'\n')
            
            listOfASBandwidthPerRelay.write(year + ',' + month + ',' + lastAS)
            listOfASBandwidthPerRelay.write(", "+ str(numRelay) +", ")
            perRelay = sumBand/(numRelay)
            listOfASBandwidthPerRelay.write(" " + str(perRelay)+'\n')
            
            numRelay = 0
            sumBand = int(currentBand)
            lastAS = currentAS
        else: 
            lastAS = currentAS
            sumBand = sumBand + int(currentBand)

    listOfASBandwidth.close()
    f.close()

if __name__ == '__main__':
    main()

