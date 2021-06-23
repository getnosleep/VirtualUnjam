"""[Docstring] Declares functions, running the heartbeat."""
from threading import Thread
from time import sleep
from paho.mqtt.client import Client, MQTTv311

class Service:
    """[Docstring] Static class, holding and managing the microservice's heartbeat thread."""
    heartbeatThread: Thread
    heartbeatCount: int

    @staticmethod
    def initiateHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> bool:
        """[Docstring] Declares functions, initiating new heartbeat with respective values."""
        Service.heartbeatThread = Thread(target=Service.publishHeartbeat, args=(interval, count, brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel, ))
        Service.heartbeatThread.daemon = True # works ONLY for generic thread class
        Service.heartbeatThread.start()
        return Service.heartbeatThread.is_alive()

    @staticmethod
    def stopHeartbeat() -> bool:
        """[Docstring] Declares functions, stopping currently running heartbeats."""
        Service.heartbeatThread.stop()
        return not Service.heartbeatThread.is_alive()

    @staticmethod
    def monitorHeartbeat() -> float:
        """[Docstring] Declares functions, fetching current heartbeat count."""
        return Service.heartbeatCount
    
    @staticmethod
    def publishHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str):
        """[Docstring] Function handling lifetime of a heartbeat."""
        try:
            Service.heartbeatCount = count
            client = Client(client_id="heartbeatPublisher",
                                    clean_session=False,
                                    userdata=None,
                                    protocol=MQTTv311,
                                    transport="tcp")
            client.username_pw_set(brokerUsername, brokerPassword)
            client.connect(brokerAddress, brokerPort, 60)
            while Service.heartbeatCount >= 0:
                Service.heartbeatCount += 1
                payload: bytes = Service.heartbeatCount.to_bytes(8, "big")
                client.publish(brokerChannel, payload=payload, qos=0, retain=False, properties=None)
                sleep(interval)
        except:
            raise Exception("EXPECTATION FAILED")
