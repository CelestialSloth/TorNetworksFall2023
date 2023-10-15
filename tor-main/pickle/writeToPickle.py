import pickle
"""Writes data from collectStream to pickle file."""
def writeToPickle(month, year):
    print("Running collectStream on listOfAS-Testing")
    ASListSorted = "listOfAS-Testing"
    #ASListSorted = "sortedListOfAS-%s-%s" %(year, month.zfill(2))
    picklefile = open('pickletest', 'wb+')

    try: 
        f = open(ASListSorted, "r")
    except (OSError, IOError):
        print("Error opening file in localGraph.py")
        print("Check if localGraph Results exists?")
        exit(1)

    start, end = getTiming(month, year) 
    nodes = {}

    for l in f:
        AS_num = l

        #Creates the stream 
        print("starting stream for %s" % AS_num)
        node = createStream(AS_num, start, end)
        nodes[AS_num] = node

        print("Writing to file")
    pickle.dump(nodes, picklefile)
    print("Finished collectStream")
    picklefile.close()
    f.close()
    return
