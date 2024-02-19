from kafka import KafkaConsumer
from pymongo import MongoClient
import json

try:
  client = MongoClient('localhost', 27017)
  db = client.captialDB
  print("Connection successful established!")
except: 
  print("Could not connect to MongoDB!")

captialConsumer = KafkaConsumer(
                    'capitals', 
                    bootstrap_servers=['localhost:9092'], 
                    auto_offset_reset='latest',
                    value_deserializer=lambda v: json.loads(v.decode('utf-8')))

for captialMessage in captialConsumer:
  jsonCapitalMessage = json.loads(captialMessage.value)
  
  try:
    dbCapitalRecord = db.capitals.insert_one(jsonCapitalMessage)
    print('inserted into mongodb', jsonCapitalMessage)
  except Exception as e: 
    print(e)
    print("Could not insert into MongoDB!")