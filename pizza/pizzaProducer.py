import random
from faker.providers import BaseProvider

# Adding a PizzaProvider with 3 methods:
#   * pizza_name to retrieve the name of the basic pizza,
#   * pizza_topping for additional toppings
#   * pizza_shop to retrieve one of the shops available
class PizzaProvider(BaseProvider):
    def pizza_name(self):
        valid_pizza_names = [
            'Margherita',
            'Marinara',
            'Diavola',
            'Mari & Monti',
            'Salami',
            'Peperoni'
        ]
        return valid_pizza_names[random.randint(0, len(valid_pizza_names)-1)]

    def pizza_topping(self):
        available_pizza_toppings = [
            'tomato',
            'mozzarella',
            'blue cheese',
            'salami',
            'green peppers',
            'ham',
            'olives',
            'anchovies',
            'artichokes',
            'olives',
            'garlic',
            'tuna',
            'onion',
            'pineapple',
            'strawberry',
            'banana'
        ]
        return available_pizza_toppings[random.randint(0, len(available_pizza_toppings)-1)]

    def pizza_shop(self):
        pizza_shops = [
            'Marios Pizza',
            'Luigis Pizza',
            'Circular Pi Pizzeria',
            'Ill Make You a Pizza You Can''t Refuse',
            'Mammamia Pizza',
            'Its-a me! Mario Pizza!'
        ]
        return pizza_shops[random.randint(0, len(pizza_shops)-1)]
      
# Import the project-related packages
from faker import Faker
import json
from kafka import KafkaProducer
import time
import random
import argparse

# Basic parameter related to the order
MAX_NUMBER_PIZZAS_IN_ORDER = 10
MAX_ADDITIONAL_TOPPINGS_IN_PIZZA = 5

# Creating a Faker instance and seeding to have the same results every time we execute the script
fake = Faker()
Faker.seed(4321)

# Adding the newly created PizzaProvider to the Faker instance
fake.add_provider(PizzaProvider)

# Creating function to generate the pizza Order
def produce_pizza_order (ordercount = 1):
    shop = fake.pizza_shop()
    # Each Order can have 1-10 pizzas in it
    pizzas = []
    for pizza in range(random.randint(1, MAX_NUMBER_PIZZAS_IN_ORDER)):
        # Each Pizza can have 0-5 additional toppings on it
        toppings = []
        for topping in range(random.randint(0, MAX_ADDITIONAL_TOPPINGS_IN_PIZZA)):
            toppings.append(fake.pizza_topping())
        pizzas.append({
            'pizzaName': fake.pizza_name(),
            'additionalToppings': toppings
        })
    # message composition
    message = {
        'id': ordercount, # Auto increment by i=i+1
        'shop': shop,
        'name': fake.unique.name(),
        'phoneNumber': fake.unique.phone_number(),
        'address': fake.address(),
        'pizzas': pizzas
    }
    key = {'shop': shop} # it can be 'id': ordercount
    return message, key


# function produce_msgs starts producing messages with Faker
def produce_msgs(hostname='localhost',
                 port='9092',
                 topic_name='pizza-orders',         # 
                 nr_messages=2,                     # Number of messages to produce (0 for unlimited)
                 max_waiting_time_in_sec=5):
    # Function for Kafka Producer with certain settings related to the Kafka's Server
    producer = KafkaProducer(
        bootstrap_servers=hostname+":"+port,
        value_serializer=lambda v: json.dumps(v).encode('ascii'),
        key_serializer=lambda v: json.dumps(v).encode('ascii')
    )
    if nr_messages <= 0:
        nr_messages = float('inf')
    i = 0
    while i < nr_messages:
        message, key = produce_pizza_order(i)

        print("Sending: {}".format(message))
        # sending the message to Kafka
        producer.send(topic_name,
                      key=key,
                      value=message)
        # Sleeping time
        sleep_time = random.randint(0, max_waiting_time_in_sec * 10)/10
        print("Sleeping for..."+str(sleep_time)+'s')
        time.sleep(sleep_time)

        # Force flushing of all messages
        if (i % 100) == 0:
            producer.flush()
        i = i + 1
    producer.flush()
    producer.close()

# calling the main produce_msgs function: parameters are:
#   * nr_messages: number of messages to produce
#   * max_waiting_time_in_sec: maximum waiting time in sec between messages


produce_msgs()