import json

from kafka import KafkaProducer
from flask import Flask, jsonify, request, g, Response

from .services import retrieve_orders, create_order

app = Flask(__name__)

@app.before_request
def before_request():
    # Set up a Kafka producer
    kafkaServer = 'localhost:9092'
    topicName = 'computer_item'
    producer = KafkaProducer(bootstrap_servers=kafkaServer)
    # producer = KafkaProducer(
    #     bootstrap_servers=kafkaServer, 
    #     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # Setting Kafka to g enables us to use this
    # in other parts of our application
    g.kafka_producer = producer
    

@app.route('/health')
def health():
    return jsonify({'response': 'Hello World!'})


@app.route('/api/orders/computers', methods=['GET', 'POST'])
def computers():
    if request.method == 'GET':
        return jsonify(retrieve_orders())
    elif request.method == 'POST':
        request_body = request.json
        result = create_order(request_body)
        return Response(status=202)
    else:
        raise Exception('Unsupported HTTP request type.')


if __name__ == '__main__':
    app.run()