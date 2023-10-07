import json

from model import Contact

from faker import Faker
import pika

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    for _ in range(5):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
        )
        contact.save()
        
        contact_id = str(contact.id)
        
        message = {
            "fullname": contact.fullname,
            "email": contact.email,
            "contact_id": contact_id
        }
        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Sent {message}")
    connection.close()

if __name__ == '__main__':
    main()
