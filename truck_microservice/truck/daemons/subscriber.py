from .callbacks import Callbacks
from paho.mqtt.client import Client, MQTTv311
from threading import Thread
from ..properties import *
import time

class Subscriber(Thread):
    def __init__(self):
        # Constructing subscriber thread
        Thread.__init__(self)
        self.__running__: bool = False
        self.__client__: Client
    
    def run(self):
        """
        Wenn wir das so machen (run ohne die underscores), sind das sogesehen override-methoden (zumindest wuerde man das in Java so nennen...)
        Somit koennen wir die normale start-Methode aus dem Thread nehmen um den run automatisch einzuleiten (die hat durch den super-Call ja ne Autoreferenz).

        Darueber hinaus glaube ich, dass es nicht reicht den self.__client__.loop_start() aufzurufen, denn das startet, so wie ich es gesehen habe,
        einen von dieser Klasse unabhaengigen Daemon. Dieser sorgt dafuer, dass der Subscriber zwar weiter zuhoert, allerdings die Werte nicht in
        diese Klasse und somit nicht in unseren Microservice zurueck gibt (wobei ich mir hierbei nicht so ganz sicher bin, ob da nicht doch irgendwo
        ein Hintertuerchen ist oder so, denn es scheint ja doch irgendwe bei dir geklappt zu haben ... Ich bin allerdings auch muede ... und
        vielleicht laber ich grade scheisse xD )

        Wie dem auch sei... morgen geht es weiter :D

        DIE LIBRARY MACHT DAS SO. die callback funktionen müssen statisch sein, mit fixen inputs (mehr oder weniger, bzw andere inputs rippen das script).
        deshalb landet der heartbeat count auf der callbacks.py als statische variable und kann von da ausgelesen werden.
        entsprechend kann auch die callback funktion angepasst werden und der wert dort direkt weitergegeben werden.
        da der loop, wie oben erwähnt, auch nebenläufig abläuft, könnte der subscriber zu einer statischen klasse verändert und dann mit callbacks zusammengelegt werden.
        dann passt der subscriber aber nicht mehr zu der daemons idee (siehe movement, lifecycle).
        """
        self.__running__ = True
        try:
            self.__client__ = Client(client_id=ID_BROKER, clean_session=False)
            self.__client__.username_pw_set(USERNAME_BROKER, PASSWORD_BROKER)
            self.__client__.on_message = Callbacks.on_message
            self.__client__.connect(ADDRESS_BROKER, PORT_BROKER)
            self.__client__.subscribe(TOPIC_BROKER)
            self.__client__.loop_start()
        except:
            pass
    
    def stop(self):
        # Function stopping subscription
        self.__running__ = False
        self.__client__.unsubscribe(TOPIC_BROKER)
        self.__client__.disconnect()
        self.__client__.loop_stop()
        time.sleep(0.100)
        # return self.__client__.is_alive()
        return not self.__client__.is_connected() # probably better than is_alive, because subscriber threads ends up in clients loop thread

def startSubscription():
    # 'Dirty starter' for subscription thread
    subscriber = Subscriber()
    subscriber.start()
    return subscriber

subscription = startSubscription()
