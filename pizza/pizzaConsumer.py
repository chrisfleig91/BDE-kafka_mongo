# Import some necessary modules
from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Connect to MongoDB and pizza_data database
try:
   client = MongoClient('localhost',27017)
   db = client.pizza_data
   print("Connected successfully!")
except:  
   print("Could not connect to MongoDB")
    
# connect kafka consumer to desired kafka topic	
consumer = KafkaConsumer('pizza-orders',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest')

# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    
    # Create dictionary and ingest data into MongoDB
    try:
      rec_id1 = db.pizza_orders.insert_one(record)
      print("Data inserted with record ids", rec_id1)
    except:
       print("Could not insert into MongoDB")