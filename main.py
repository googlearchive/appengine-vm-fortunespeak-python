from oauth2client.client import GoogleCredentials

__author__ = 'waprin'

from gcloud import pubsub
from gcloud import datastore
import json

from flask import Flask


PROJECT_ID = "silver-python2"
TOPIC_NAME = "demonstration-topic"
SUBSCRIPTION_NAME = "java-subscription"

def get_topic():
    """Gets the configured topic, creating it if needed."""
    topic = pubsub.Topic(TOPIC_NAME)
    if not topic.exists():
        topic.create()

    return topic

def get_subscription():
    """Gets the configured subscription, creating it if needed."""
    topic = get_topic()

    subscription = pubsub.Subscription(SUBSCRIPTION_NAME, topic)

    if not subscription.exists():
        subscription.create()

    return subscription


def queue_book():
    """
    Queues a book for background processing. This publishes a message
    containing the book's ID to the configured pubsub topic. Any worker
    instances can receive this message via their shared subscription.
    """
    key = datastore.Key('Book')

    entity = datastore.Entity(key=key)

    data = {
        'status': 'UNPROCESSED'
    }
    entity.update(data)
    datastore.put(entity)
    data['id'] = entity.key.id

    topic = get_topic()
    topic.publish(json.dumps(data).encode('utf-8'))

    key = datastore.Key('Book', entity.key.id)

    results = datastore.get(key)

    return entity.key.id



datastore.set_defaults(dataset_id=PROJECT_ID)

credentials = GoogleCredentials.get_application_default()
pubsub.set_default_connection(pubsub.Connection(credentials))
pubsub.set_default_project(PROJECT_ID)

app = Flask(__name__)




@app.route('/publish')
def publish():
    id = queue_book()
    return str(id)

@app.route('/status/<int:id>')
def get_status(id):
    key = datastore.Key('Book', id)
    result = datastore.get(key)
    print('result is {}'.format(result))
    return result['status']

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
