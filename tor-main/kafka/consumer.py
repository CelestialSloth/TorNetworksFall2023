#https://docs.confluent.io/kafka-clients/python/current/overview.html
from sys import argv
from confluent_kafka import Consumer, OFFSET_BEGINNING, avro
from AS_nodes import *
import msgpack
import json

"""Read messages from localGraph through kafka. 
ARGV:
    topic: array of kafka topic(s) to subscribe to
"""
def receiveKafka(topic):
    consumer = Consumer(
        {'bootstrap.servers': 'localhost:9092',
        'group.id': "foo",
        'auto.offset.reset': 'earliest',
        })
    consumer.subscribe(topic)

    kafkaFile = "data/data.json"
    json_dict = {"ASNs": []}

    try:
        while True:
            msg = consumer.poll(5.0)
            if msg is None:
                print("waiting")
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                AS_dict = msgpack.unpackb(msg.value(), raw=False)
                json_dict["ASNs"].append(AS_dict) #Save to json, figure out best way, or sqlite
                #for key in AS_dict.keys():
                    # json.dump(key, f) #key = ASN-Bandwidth
                    # json.dump(AS_dict[key], f)
                    #print(key)
                    #node = AS_node(key[:-1])
                    #for p in AS_dict[key]:
                        #node.addPath(p)
                #print(node.ASN)
                #print(node.paths)

                #Can save as local graph, get the bc, etc
                #node.saveLocalGraph()
                #bc = node.get_BC()
                #print("for %s: BC of %f" %(node.ASN, bc))
    except KeyboardInterrupt:
        consumer.close()
        f.close()
        pass
    finally:
        consumer.close()
        f.close()
    
    with open(kafkaFile, "w") as f:
        json.dump(json_dict, f)

def main():
    topic = ["test"]
    receiveKafka(topic)
    
if __name__ == "__main__":
    main()