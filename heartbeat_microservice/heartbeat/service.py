"""[Docstring] Declares functions, running the heartbeat."""
from threading import Thread
from time import time

from paho.mqtt.client import Client, MQTTv311
#from .heartbeat import Heartbeat



class Service:
    """[Docstring] Static class, holding and managing the microservice's heartbeat thread."""

    #heartbeatThread: Heartbeat
    heartbeatThread: Thread
    heartbeatCount: float

    @staticmethod
    def initiateHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> bool:
        """[Docstring] Declares functions, initiating new heartbeat with respective values."""
        #Service.heartbeatThread = Heartbeat(interval, count, brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel)
        #return Service.heartbeatThread.start()
        Service.heartbeatThread = Thread(target=Service.publishHeartbeat, args=(interval, count, brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel))
        # Start thread in thread to make eternal loop parallel
        Thread(target=Service.heartbeatThread.start())
        if Service.heartbeatThread.is_alive():
            return True
        else:
            return False

    @staticmethod
    def stopHeartbeat() -> bool:
        """[Docstring] Declares functions, stopping currently running heartbeats."""
        return Service.heartbeatThread.stop()

    @staticmethod
    def monitorHeartbeat() -> float:
        """[Docstring] Declares functions, fetching current heartbeat count."""
        return Service.heartbeatCount

    @staticmethod
    def publishHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> None:
        """[Docstring] Function handling lifetime of a heartbeat."""
        try:
            Service.heartbeatCount = count
            running = True
            client = Client(client_id="heartbeatPublisher",
                                    clean_session=False,
                                    userdata=None,
                                    protocol=MQTTv311,
                                    transport="tcp")
            client.username_pw_set(brokerUsername, brokerPassword)
            client.connect(brokerAddress, brokerPort, 60)
            while running:
                Service.heartbeatCount += 1
                payload: bytes = Service.heartbeatCount.to_bytes(2, "big")
                client.publish(brokerChannel, payload=payload, qos=0, retain=False, properties=None)
                time.sleep(interval)
        except Exception:
            running = False
            raise Exception("EXPECTATION FAILED")