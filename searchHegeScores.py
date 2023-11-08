import sys
import msgpack
import argparse
import csv

from confluent_kafka import Consumer, TopicPartition, KafkaError

"""
Use this code to search through the as hegemony scores in the ihr_hegemony
kafka topic. This assumes that the ihr_hegemony kafka topic has been
populated by running the scripts in the as-hegemony repository.

Example to run this code:
$ python3 searchHegeScores.py --asn 12552
You can specify server with the --server flag, number of partitions with
the --partitions flag.

Output:
* This code will print a dictionary of information about the asn, including
the hegemony score, if the asn is found in the data.
* If the asn isn't found, nothing is printed.
"""

# def searchByASNKafka(asn, topic, num_partitions, server):
# searches through the kafka messages in ihr_hegemony for the given asn
def searchByASN(asn, num_partitions, server):
    topic = 'ihr_hegemony'

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ihr_tail',  # does this need to be named this?
        'enable.auto.commit': False,
    })

    partition = TopicPartition(topic, num_partitions)
    low, high = consumer.get_watermark_offsets(partition)
    partition = TopicPartition(topic, num_partitions, low)
    consumer.assign([partition])

    i = 0
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
        if data['asn'] == str(asn):
            print(msgdict)
            break

        i += 1
        if i >= high:
            break

    consumer.close()

# populates a csv file 'hegemonydata.csv' with a list of {asn, hege} values
# not currently used
def downloadDataToFile():

    server = 'localhost:9092'
    num_partitions = 0
    topic = 'ihr_hegemony'

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ihr_tail',  # does this need to be named this?
        'enable.auto.commit': False,
    })

    partition = TopicPartition(topic, num_partitions)
    low, high = consumer.get_watermark_offsets(partition)
    partition = TopicPartition(topic, num_partitions, low)
    consumer.assign([partition])

    with open('hegemonydata.csv', 'a', newline='') as file:
        file.truncate(0)  # delete old contents
        writer = csv.writer(file)
        i = 0
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
            writer.writerow([data['asn'], data['hege']])

            i += 1
            if i >= 5:
                break

        consumer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='localhost:9092')
    parser.add_argument('-p', '--partitions', default=0)
    parser.add_argument('-n', '--asn')
    # parser.add_argument('-t', '--topic', default='ihr_hegemony')
    args = parser.parse_args()
    assert args.asn

    # searchByASNKafka(args.asn, args.topic, args.partitions, args.server)
    searchByASN(args.asn, args.partitions, args.server)