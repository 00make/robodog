import roslibpy
from .connection import ROSConnection

class DogStateSubscriber:
    def __init__(self, dog):
        self.dog = dog
        self._conn = ROSConnection()
        self.topics = {
            'ctrl_state': '/alphadog_node/dog_ctrl_state',
            'body_status': '/alphadog_node/body_status'
        }
        self._subscribers = {}

    def subscribe_ctrl_state(self, callback=None):
        def default_callback(message):
            if isinstance(message, dict) and 'state' in message:
                self.dog.update_ctrl_state(message['state'])
            else:
                print("Warning: Invalid ctrl_state message format")

        topic = self.topics['ctrl_state']
        listener = roslibpy.Topic(
            self._conn.client,
            topic,
            'ros_alphadog/DogCtrlStateStamped'
        )
        listener.subscribe(callback or default_callback)
        self._subscribers[topic] = listener

    def subscribe_body_status(self, callback=None):
        def default_callback(message):
            if isinstance(message, dict) and 'status' in message:
                self.dog.update_body_status(message['status'])
            else:
                print("Warning: Invalid body_status message format")

        topic = self.topics['body_status']
        listener = roslibpy.Topic(
            self._conn.client,
            topic,
            'ros_alphadog/BodyStatusStamped'
        )
        listener.subscribe(callback or default_callback)
        self._subscribers[topic] = listener

    def unsubscribe_all(self):
        for topic in self._subscribers.values():
            topic.unsubscribe()