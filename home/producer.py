import pika, json

params = pika.URLParameters('amqps://cpmlzpub:3w_6oIhfQ6rPTNU76baCy07V5fDeOjNi@beaver.rmq.cloudamqp.com/cpmlzpub')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    print(method, body)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
