import pika
import json
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from bson import ObjectId

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

def process_quote(quote_data):
    author_name = quote_data['author']
    author = Author.objects.get(fullname=author_name)
    
    quote = Quote(
        quote=quote_data['quote'],
        author=author,
        tags=quote_data['tags']
    )
    quote.save()
    print(f"Цитата збережена у базі даних: {quote.quote}")

def callback(ch, method, properties, body):
    quote_data = json.loads(body)
    process_quote(quote_data)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='quotes')

channel.basic_consume(queue='quotes', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень з черги RabbitMQ...')

channel.start_consuming()