import GPIO as GPIO
import threading
import time
import socket as sk

class Board:
    channelConfigs = {}
    channelEvents = {}
    __instance = None
    serviceThread = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Board.__instance == None:
            Board()
        return Board.__instance
    
    def __init__(self):
        if Board.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Board.__instance = self

#             global serviceThread
            Board.__instance.serviceThread = ServiceThread()
#             serviceThread.piBoardCallback = piBoardCallback
            Board.__instance.serviceThread.setPiBoardCallback(Board.__instance.piBoardCallback)
            Board.__instance.serviceThread.threadify()
           
    def piBoardCallback(val):
        print "piBoardCallback"
        
        global channelEvents
        # This assumes that val is in format {channel:[HI|LOW]}
        x = val.split(":")
        print(val)
        channel = x[0]
        edge = x[1]
        print(channel)
        print(edge)
        
        event = channelEvents[channel]
        print(event)
    
    def setChannelConfig(self, channel):
        if channel != None:
            self.channelConfigs[channel.chanel] = channel
        
    def setChannelEvent(self, channel, edge, eventCallback):
        if channel != None:
            event = Event(edge,eventCallback)
            self.channelEvents[channel] = Event(edge,eventCallback)
   
class Event:

    eventCallback = None
    edge = None

    def __init__(self,_edge,_eventCallback):
        global edge
        global eventCallback
        edge = _edge
        eventCallback = _eventCallback 
    
    def getEventCallback():
        return self.eventCallback
   
    def setEventCallback(eventCallback):
        self.eventCallback = eventCallback
   
class Service:
 
    serviceThreadCallback = None
 
    def __init__(self):
        print "Service __init__"
        
    def listen(self,_serviceThreadCallback):
        global serviceThreadCallback
        serviceThreadCallback = _serviceThreadCallback
        connection = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        connection.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        connection.bind(('0.0.0.0', 5566))
        connection.listen(10)
        while True:
            current_connection, address = connection.accept()
            while True:
                data = current_connection.recv(2048)
    
                if data == 'quit\\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                    break
    
                elif data == 'stop\\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                    exit()
    
                elif data:
                    serviceThreadCallback(data)
                    
                else:
                    break         
    
    def setCallback(_serviceThreadCallback):
        global serviceThreadCallback
        serviceThreadCallback = _serviceThreadCallback
        
#     def getCallback(serviceThreadCallback):
#         return self.serviceThreadCallback
        
class ServiceThread:

    thread = None
    svc = None
    piBoardCallback = None

    def __init__(self, interval=1):
        self.interval = interval

    def run(self):
            global piBoardCallback
            self.svc = Service()
            self.svc.listen(piBoardCallback)

    def setPiBoardCallback(__X, _piBoardCallback):
        global piBoardCallback
        piBoardCallback = _piBoardCallback
 
#     def getPiBoardCallback():
#         return self.piBoardCallback
        
    def threadify(self):
        print("threadify")
        print(self)
        global thread
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        
    def serviceThreadCallback(val):
        self.piBoardCallback(val)


def ext_callback(val):
    print "ext_callback"
    print val        
                
if __name__ == '__main__': 
     
    try:
        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.IN, 0, GPIO.PUD_UP)
            GPIO.add_event_detect(22, GPIO.FALLING, ext_callback, bouncetime=1500)
            time.sleep(1000)
    except KeyboardInterrupt:
        pass      
