from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Post, Like
import pika
import json
def publish_message(message):
    params = pika.URLParameters('amqps://cpmlzpub:3w_6oIhfQ6rPTNU76baCy07V5fDeOjNi@beaver.rmq.cloudamqp.com/cpmlzpub')

    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    message = {
        "data" : 1,
        "fruits" : ["apple", "banana"]
    }
    channel.basic_publish(exchange='',
                          routing_key='my_queue',
                          body=json.dumps(message),
                        )
    print(f"Published message: {message}")
    connection.close()



def post_list(request):
    publish_message('Hello, RabbitMQ!')
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})
