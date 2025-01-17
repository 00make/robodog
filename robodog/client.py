import roslibpy
from typing import Any, Callable
from .connection import ROSConnection

class ROSClient:
    """ROS client wrapper class"""
    
    def __init__(self, host: str = '10.10.10.10', port: int = 9090):
        self._conn = ROSConnection()
        self._conn.setup(host, port)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to ROS server"""
        self._conn.connect()

    def disconnect(self):
        """Disconnect from ROS server"""
        self._conn.disconnect()

    def reconnect(self):
        """Reconnect to ROS server"""
        self._conn.reconnect()

    @property
    def client(self):
        """Get underlying ROS client instance"""
        return self._conn.client

    def publish(self, topic: str, msg_type: str, message: dict) -> None:
        """Publish message to topic"""
        publisher = roslibpy.Topic(self.client, topic, msg_type)
        try:
            publisher.publish(message)
        finally:
            publisher.unadvertise()

    def call_service(self, service: str, service_type: str, request: dict) -> dict:
        """Call service"""
        service_client = roslibpy.Service(self.client, service, service_type)
        return service_client.call(request)