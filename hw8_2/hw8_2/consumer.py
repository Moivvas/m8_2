import time
import json

import pika
from mongoengine import *
from model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def send_email(email):
    pass

def update_contact_field(contact_id):
    

    connect(host="mongodb+srv://moivvas:moivvaspassword@cluster0.4mzl2qs.mongodb.net/?retryWrites=true&w=majority")

    try:
        contact = Contact.objects.get(id=contact_id)
        contact.confirm = True
        contact.save()
        print(f" [x] Updated contact {contact_id}")
    except Contact.DoesNotExist:
        print(f" [x] Contact {contact_id} not found in the database")

def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    
    fullname = message.get("fullname")
    email = message.get("email")
    contact_id = message.get("contact_id")
    
    print(f" [x] Sending message to {fullname} with email {email}")
    send_email(email)
    update_contact_field(contact_id)
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
