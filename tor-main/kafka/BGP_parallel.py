#from localGraph import *
from multiprocessing import Pool
from datetime import datetime
import argparse
from AS_nodes import *
from producer import *
import pybgpstream 
import json

""" Returns a AS_node with the paths originating from AS_num from a bgpstream from start to end.

    ARGS:
        AS_num: The AS number to filter for
        start: 
        end:
"""
def createStream(AS_num, start, end):
    node = AS_node(AS_num)
    stream = pybgpstream.BGPStream(
            from_time = start, until_time = end,
            #for now use all: later, filter out some (biased),  
            collectors = ["route-views.sg"],
            record_type = "ribs",
            filter = "path _%s$" % AS_num[:-1]
        )
    print("Finding elems:")
    x = 0
    for elem in stream:
        x += 1
        if (x > 5):
            break
        if elem.fields["prefix"] == "0.0.0.0/0":
            continue
        path = elem.fields["as-path"]
        if len(path) <= 1:
            continue
        node.paths.append(path)
    print("Finished stream for ", AS_num)
    return node

"""
Using a sorted list of ASNs, it calls createStream() on each ASN
to find paths that originate from one of the listed ASNs.

    ARGS:
        month: string
        year: string
"""
def collectStream(month, year, bandwidth):
    print("Running collectStream on listOfAS-Testing")
    #ASListSorted = "listOfAS-Testing"
    ASListSorted = "data/formatted/asLists/sortedListOfAS-%s-%s" %(year, str(month).zfill(2))
    
    results = "localGraphResults-%s-%s" % (year, str(month).zfill(2))
    r = open(results, "w+")
    f = openFile(ASListSorted)

    start, end = getTiming(month, year) 

    for l in f:
        line = l.split(" ")
        if len(line) <= 1:    # <--- to look at bandwidth
            bandwidth = "" 
        else:
            bandwidth = line[1]
        AS_num = line[0]
        node = createStream(AS_num, start, end)
        node.bandwidth = bandwidth
        node.writeToFile(r)
        print("Writing to file")

    print("Finished collectStream")
    r.close()
    f.close()
    return

"""Given an ASN, it create BGPstream and sends the paths found originating
from the ASN through a kafka producer.

ARGS:
    ASN: int 
    start
    end

"""
def sendASNtoKafka(ASN:int, start, end):
    topic = "test"
    producer = Producer(
        {'bootstrap.servers': 'localhost:9092',
        'default.topic.config': {'compression.codec': 'snappy'}
        }) 
    print(ASN, start, end)
    node = createStream(ASN, start, end)
    AS_dict = {node.ASN: node.paths}
    producer.produce(
            topic, 
            msgpack.packb(AS_dict, use_bin_type=True), 
            callback=on_commit
            )
    producer.flush()

def sendASNtoKafkaBandwidth(ASN:int, bandwidth:int, start, end):
    topic = "test"
    producer = Producer(
        {'bootstrap.servers': 'localhost:9092',
        'default.topic.config': {'compression.codec': 'snappy'}
        }) 
    print(ASN, start, end)
    node = createStream(ASN, start, end)
    key = "{}-{}".format(node.ASN, bandwidth)
    AS_dict = {key: node.paths}
    producer.produce(
            topic, 
            msgpack.packb(AS_dict, use_bin_type=True), 
            callback=on_commit
            )
    producer.flush()

#TODO: finish function
def writeASNtoJSON(month, year):
    startTiming = datetime.now()
    print("Writing to JSON on %s, %s" %(month, year))
    start, end = getTiming(month, year) 

    #ASListSorted = "../data/formatted/asLists/sortedListOfAS-%s-%s" %(year, month.zfill(2))
    ASListSorted = "listOfAS-Testing"
    asList = openFile(ASListSorted)
    jsonFile = "data/json/" + start[0:7] + ".json"

    json_dict = {"ASNs": []}
    for l in asList:
        line = l.split(" ")
        AS_num = line[0]
        bandwidth = line[1][:-2]
        node = createStream(AS_num, start, end)
        key = "{}-{}".format(node.ASN, bandwidth)
        AS_dict = {key: node.paths}
        json_dict["ASNs"].append(AS_dict)

    with open(jsonFile, "w") as jsonF:
        json.dump(json_dict, jsonF, indent=2)

def startRunningParallel(month, year, bandwidth):
    bandwidth = True
    startTiming = datetime.now()
    print("Running in parallel on %s, %s" %(month, year))
    print("bandwidth: ",  bandwidth)
    start, end = getTiming(month, year) 
    
    #ASListSorted = "../data/formatted/asLists/sortedListOfAS-%s-%s" %(year, month.zfill(2))
    ASListSorted = "listOfAS-Testing"
    f = openFile(ASListSorted)

    #Using parallel processes
    info = []
    for l in f:
        line = l.split(" ")
        AS_num = line[0]
        if bandwidth:    # <--- to look at bandwidth
            bandwidth = line[1]
            info.append((AS_num, bandwidth, start, end))
        else:
            info.append((AS_num, start, end))
        print(AS_num)

    print("Starting Processes")
    if kafka:
        if bandwidth:
            with Pool(processes=32) as pool:
                pool.starmap(sendASNtoKafkaBandwidth, info)
                pass
        else:
            with Pool(processes=32) as pool:    
                pool.starmap(sendASNtoKafka, info)
                pass

    endTiming = datetime.now()
    print("Execution time:",
      str(endTiming-startTiming)[5:])
    return

"""
Sends bandwidth of an AS through kafka
"""
def runMultiple(startMonth, startYear, endMonth, endYear, bandwidth, kafka):
    print("Running in parallel on %i, %i to %i, %i" %(startMonth, startYear, endMonth, endYear))
    while ((startYear < endYear ) or (startMonth <= endMonth and startYear == endYear )):
        if kafka:
            startRunningParallel(startMonth, startYear, bandwidth)
        else:
            writeASNtoJSON(startMonth, startYear)
        #print(startMonth, startYear)
        startMonth += 1
        if (startMonth == 13):
            startYear += 1
            startMonth = 1
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=int, required=True, nargs = 2)
    parser.add_argument('-e', type=int, default=None, nargs = 2)
    #TODO: fix -b option
    parser.add_argument('-b', type=bool, default=False, nargs = 1)
    parser.add_argument('-k', type=bool, default=False, nargs = 1)
    args = parser.parse_args()  

    startMonth = args.s[0]
    startYear = args.s[1]
    endMonth = startMonth if args.e is None else args.e[0]
    endYear = startYear if args.e is None else args.e[1]
    bandwidth = args.b[0]
    kafka = args.k
    print("Kafka: ", kafka)
    print("Finding bandwidth: ", bandwidth)
    runMultiple(startMonth, startYear, endMonth, endYear, bandwidth, kafka)
        
    return

if __name__ == "__main__":
    main()