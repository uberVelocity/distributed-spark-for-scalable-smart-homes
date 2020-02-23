from kafka import KafkaConsumer
from json import loads


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('historical',
                         group_id='spark_test_worker',
                         bootstrap_servers=['kafka:29091'],
                         key_deserializer=lambda m: m.decode(),
                         value_deserializer=lambda m: loads(m.decode('ascii')))

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
