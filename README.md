# Kafka Developer Harness

_v0.2.0 - Updated 31 October 2022_

This is inteded to be a quick start project to jump start local Kafka development. It includes the following components:

1. Launch a containerized local Kafka server + Zookeeper environment.
2. Simple Kafka producer CLI that pushes fake messages into a topic.
3. Simple Kafka consumer CLI that consumes available messages from a topic.

## Requirements
* [Poetry](https://python-poetry.org/)
* [Docker](https://docs.docker.com/get-docker/)

## Give it a spin
### Kafka server
* Spin up the kafka server stack<br/>
```./scripts/kafka-server-ctl.sh```

* Shut down the kafka server stack<br/>
```./scripts/kafka-server-ctl.sh down```

* Run the kafka server stack in detached mode<br/>
```./scripts/kafka-server-ctl.sh up -d```

### Kafka producer
* Run the producer in verbose mode with default options (helper script)<br/>
```./scripts/kafka-producer.sh --verbose```

* See help options for producer<br/>
```./scripts/kafka-producer.sh -h```

### Kafka consumer
* Run the consumer in verbose mode with default options (helper script)<br/>
```./scripts/kafka-consumer.sh --verbose```

* See help options for consumer<br/>
```./scripts/kafka-consumer.sh -h```

### Makefile
* Makefile usage<br/>
```make```

* Prep the environment<br/>
```make install```

* Test the producer and consumer<br/>
```make test```

* Clean the environment<br/>
```make clean```


## Tools
* [kcat CLI (formerly kafkacat)](https://github.com/edenhill/kcat) for testing and debuging Apache Kafka® deployments. [Learn how to use it with Confluent](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html#kcat-formerly-kafkacat-utility). 
* [Offset Explorer (formerly Kafka Tool)](https://www.kafkatool.com/) is a GUI application for managing Kafka clusters.
