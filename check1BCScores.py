import sys
import msgpack
import argparse
import csv

from confluent_kafka import Consumer, TopicPartition, KafkaError

"""
This script determines what fraction of a particular BCScore topic has
Scores of 1. Note that each ASN is listed multiple times, possibly with 
different BCScores, and we aren't checking for unique ASNs.

Example to run this code:
$ python3 check1BCScores.py
You can specify server with the --server flag, number of partitions with
the --partitions flag.

Output:
* This code will print a dictionary of information about the asn if the asn is found in the data.
* If the asn isn't found, nothing is printed.
"""

# searches through the kafka messages in ihr bcscore topic for the given asn
def searchBCScores(num_partitions, server, topic):

    consumer = Consumer({
        'bootstrap.servers': server,
        'group.id': 'ihr_tail',  # does this need to be named this?
        'enable.auto.commit': False,
    })

    partition = TopicPartition(topic, num_partitions)
    low, high = consumer.get_watermark_offsets(partition)
    partition = TopicPartition(topic, num_partitions, low)
    consumer.assign([partition])

    numBCScores = 0
    num1BCScores = 0
    i = 0
    asnsWithNon1BC = []
    while True:
        msg = consumer.poll(1000)
        msgdict = {
            'topic': msg.topic(),
            'partition': msg.partition(),
            'key': msg.key(),
            'timestamp': msg.timestamp(),
            'headers': msg.headers(),
            'value': msgpack.unpackb(msg.value(), raw=False)
        }
        data = msgdict['value']
        for asn in data['bcscore'].keys():
            bcscore = data['bcscore'][asn]
            numBCScores += 1
            if bcscore == 1.0:
                num1BCScores += 1
            else:
                asnsWithNon1BC.append(asn)


        i += 1
        if i >= high:
            
            print("Number of 1.0 BC scores: " + str(num1BCScores))
            print("Total number of BC scores: " + str(numBCScores))
            print("Fraction of BC scores that are 1.0: ")
            print(num1BCScores/numBCScores)
            print("Note that each ASN might contribute multiple BC scores to this total")
            break

    consumer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='localhost:9092')
    parser.add_argument('-p', '--partitions', default=0)
    parser.add_argument('-t', '--topic', default='ihr_bcscore_rrc10')
    args = parser.parse_args()

    # searchByASNKafka(args.asn, args.topic, args.partitions, args.server)
    searchBCScores(args.partitions, args.server, args.topic)
