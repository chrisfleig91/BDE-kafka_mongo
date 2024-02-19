from kafka import KafkaProducer
import pandas as pd
import json
import time
import random

captialsCsv = "./files/city-populations.csv"

captialsDF = pd.read_csv(captialsCsv)

def produce_messages(hostname='localhost', port='9092', topic_name='capitals'):
  producer = KafkaProducer(
        # localhost:9092
        bootstrap_servers=hostname+":"+port,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
  
  for index, capital in captialsDF.iterrows():
    print("Sending: {}".format(capital.to_json()))
    # sending the message to Kafka
    producer.send(topic_name,
                  key={ 'capital': random.randint(0, 10000000)},
                  value=capital.to_json())
    # Sleeping time
    print("Sleeping for..."+str(1)+'s')
    time.sleep(1)
  
  producer.flush()
  producer.close()

produce_messages()