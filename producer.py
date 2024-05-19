import pika
import json
from mongoengine import connect, Document, StringField, ReferenceField, ListField

# Підключення до MongoDB
connect("mongodb+srv://XenKos:<kseni4ka78>@cluster0.02433gx.mongodb.net/XenKos?retryWrites=true&w=majority")

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author)
    tags = ListField(StringField())

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='quotes')

quotes = Quote.objects()
for quote in quotes:
    quote_data = {
        'quote': quote.quote,
        'author': quote.author.fullname,
        'tags': quote.tags
    }
    channel.basic_publish(exchange='', routing_key='quotes', body=json.dumps(quote_data))

print("Цитати надіслані в чергу RabbitMQ")

connection.close()