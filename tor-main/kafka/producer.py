from confluent_kafka import Producer
import msgpack

"""Run when producer sends a message through kafka.
Reports either an error or successful commit.
"""
def on_commit(err, par):
    if err:
        print('Message failed: {}'.format(err))
    else:
        print("Commit successful: " + str(par))

"""
Creates basic example producer.
"""
def createProducer():
    producer = Producer(
            {'bootstrap.servers': 'localhost:9092',
            })
    producer.poll(0)
    return producer

def produce(producer, topic, node):
    producer.produce(topic, msgpack.packb(node), callback=on_commit)
    producer.poll(10000)
    producer.flush()

    return

def main():
    #produce()
    pass

if __name__ == "__main__":
    main()