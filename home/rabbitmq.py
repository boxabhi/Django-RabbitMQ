# posts/consumer.py

import pika
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_like_app.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Post, Notification

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    liked_by_id, post_id = message.split(' liked post ')
    liked_by_id = int(liked_by_id)
    post_id = int(post_id)

    post = Post.objects.get(id=post_id)
    liked_by = User.objects.get(id=liked_by_id)

    notification_message = f"{liked_by.username} liked your post '{post.title}'"
    Notification.objects.create(user=post.author, message=notification_message)

    print(f"Notification sent: {notification_message}")

def start_consumer():
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='post_likes')
    channel.basic_consume(queue='post_likes', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
