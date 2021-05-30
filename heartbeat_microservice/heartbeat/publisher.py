"""[Docstring] Declares functions, publishing the heartbeat."""
from paho.mqtt.client import Client

class Publisher(object):
    """[Docstring] Declares functions, publishing the heartbeat."""

    def __init__(self, client: Client, brokerAddress: str, port: int, channel: str):
        """[Docstring] Function constructing object."""
        self.__client__ = client
        self.__brokerAddress__ = brokerAddress
        self.__port__ = port
        self.__channel__ = channel
    
    def setClient(self, client: Client):
        """[Docstring] Function setting new channel for leader."""
        self.__client__ = client

    def getClient(self):
        """[Docstring] Function getting leader's channel."""
        return self.__client__

    def setChannel(self, channel: str):
        """[Docstring] Function setting new channel for leader."""
        self.__channel__ = channel

    def getChannel(self):
        """[Docstring] Function getting leader's channel."""
        return self.__channel__
    
    def establishConnectionToBroker(self):
        """[Docstring] Function connecting client to broker."""
        self.__client__.connect(self.__brokerAddress__,
                                port = self.__port__,
                                keepalive = 60,
                                bind_address='',
                                bind_port=0
                                )
        return self.__client__.is_connected()
    
    def suspendConnectionToBroker(self):
        """[Docstring] Function cutting connection to broker."""
        self.__client__.disconnect()
        return not self.__client__.is_connected()
    
    def publishHearbeatToChannel(self, count: int):
        """[Docstring] Function publishing the heartbeat."""
        message = bytes(count)
        val = self.__client__.publish(self.__channel__, payload=message, qos=0, retain=False)
        return val.is_published()