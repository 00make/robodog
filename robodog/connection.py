import roslibpy
from typing import Optional

class ROSConnection:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ROSConnection, cls).__new__(cls)
            cls._instance.host = '10.10.10.10'  # Default value
            cls._instance.port = 9090           # Default value
        return cls._instance

    def setup(self, host: str = '10.10.10.10', port: int = 9090):
        """Initialize connection configuration"""
        self.host = host
        self.port = port
        # If there is already a connection, reconnect using the new configuration
        if self._client and self._client.is_connected:
            self.reconnect()

    def connect(self):
        if not self._client:
            self._client = roslibpy.Ros(host=self.host, port=self.port)
            self._client.run()

    def disconnect(self):
        """Disconnect from ROS server"""
        if self._client and self._client.is_connected:
            self._client.terminate()
            self._client = None

    def reconnect(self):
        """Reconnect to ROS server"""
        self.disconnect()
        self.connect()

    @property
    def client(self):
        """Get ROS client instance"""
        if not self._client or not self._client.is_connected:
            raise ConnectionError("ROS client not connected")
        return self._client

    @property
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._client is not None and self._client.is_connected
