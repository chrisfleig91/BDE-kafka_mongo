# BDE-kafka_mongo

Dieses Repository dient dem Zweck beispielhaft zu zeigen, wie Daten über einen Apache Kafka Producer in ein Apache Kafka Topic zu schreiben und aus diesem per Consumer, die Daten wieder auszulesen.

Danach sollen die Daten über den Consumer in eine MongoDB geschrieben werden.

## Programmiersprache

Python

## Installierte Software

1. anaconda
2. Docker Desktop: Zum Starten von Docker Containern
3. MongoDB
4. Apache Kafka über Docker Container
5. Visual Studio Code oder eine vergleichbare IDE

## Steps

### git repository klonen

1. Dieses Repository auf lokale Maschine klonen
  `git clone https://github.com/chrisfleig91/BDE-kafka_mongo.git`

### anaconda environment

1. Mittels anaconda ein neues environment erstellen mit Python Version 3.11.7:
  `conda create -n kafka-mongo-env python=3.11.7`
2. conda-forge repository hinzufügen in conda:
  `conda config --add channels conda-forge`
3. dependencies installieren
  `conda install --name kafka-mongo-env pymongo kafka-python pandas faker`
4. Alternative zu 1., 2. & 3.:
  `conda env create -f environment_kafka-mongo.yml`

## Installieren von MongoDB Community

**Ganz wichtig:** *wir benutzen hier eine lokale MongoDB Community und kein cloudbasiertes MongoDB Atlas oder ein MongoDB Enterprise*

[Installation von MongoDB Community](https://www.mongodb.com/docs/manual/installation/)
Nach der Installation sollte MongoDB Community auf Port 27017 laufen.
Am besten gleich während der Installation auch MongoDB Compass installieren als grafische Datenbank IDE für MongoDB.
Kommt über einen Haken beim Setup mit.

## Installieren von Docker Desktop

[Installation von Docker Desktop](https://docs.docker.com/get-docker/)  

## Setup Apache Kafka und Zookeeper Container über Docker

[Setup Apache Kafka über Docker](https://www.conduktor.io/kafka/how-to-start-kafka-using-docker/)
Folgt dem Link, um eine lauffähige Kafka und Zookeeper Container Instanz bei eich laufen zu lassen.
Es ist wirklich sehr simpel, folgt einfach den Anleitungen.

Danach die Container für Apache Kafka und Zookeeper über Docker Desktop laufen lassen.

## Erstellen der Topics in Apache Kafka

Jetzt müssen die Kafka Topics für den Producer und Consumer erstellt werden. Dafür müssen die Docker Container laufen.
Die Kafka Topics können entweder über die Docker Exec Konsole in Docker Desktop im kafka1 Container erstellt werden.
Oder es wird eine Verbindung per Kommandozeile auf den kafka1 Container hergestellt: `docker exec -it kafka1 /bin/bash`

Danach dann per folgenden Befehlen die beiden Topics für "pizza-orders" und "capitals" erstellen:
`kafka-topics --create --topic capitals --bootstrap-server localhost:9092`
`kafka-topics --create --topic pizza-orders --bootstrap-server localhost:9092`

## Starten des Programms

Über die *Producer.py Dateien können entsprechende Daten in die Topics geschrieben werden.
Einfach im Environment laufen lassen mit `python pizzaProducer.py` oder `python capitalProducer.py`

Falls Ihr testen wollt, ob etwas im Topic ankommt, könnt ihr im Docker Container die folgenden Befehle laufen lassen:
`kafka-console-consumer --topic pizza-orders --bootstrap-server localhost:9092`
`kafka-console-consumer --topic capitals --bootstrap-server localhost:9092`

Diese Befehle starten einen Listener, der ausgibt, was alles im Topic ankommt.

Wenn Daten angekommen sind, können diese dann über die *Consumer.py abgerufen und in die MongoDB geschrieben werden.
Die Skripte auch wieder im Environment mit folgenden Befehlen laufen lassen `python pizzaConsumer.py` oder `python capitalConsumer.py`

## Testen, ob Daten in MongoDB angekommen sind

Per MongoDBCompass auf den Port 27017 verbinden und dann schauen, ob es zwei neue Datenbanken namens "pizza_data" und "capitalDB" mit den entsprechenden Collections gibt.

## Link zum Online Video findet ihr im DBUAS Kurs "Big Data Engineering" unter Präsenzvorlesung
