import threading
import time

import GPIO as GPIO
import socket as sk


class Board:
    channelConfigs = None
    channelEvents = None
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
            Board.__instance.channelEvents = {}
            Board.__instance.channelConfigs = {}
            Board.__instance.serviceThread = ServiceThread()
            Board.__instance.serviceThread.setPiBoardCallback(Board.__instance.piBoardCallback)
            Board.__instance.serviceThread.threadify()
           
    def piBoardCallback(_piBoardInstance, _value):
        
        global channelEvents
        # This assumes that val is in format {channel:[HI|LOW]}, i.e. 22:HI
        values = _value.split(":")
        channel = values[0]
        edge = values[1]
        
        event = _piBoardInstance.channelEvents[int(channel)]
        # TODO: Handle logic on wheter to call event callback or not.
        event.eventCallback(event)
    
    def setChannelConfig(_piBoardInstance, channel):
        if channel != None:
            _piBoardInstance.channelConfigs[channel.chanel] = channel
        
    def setChannelEvent(_piBoardInstance, _channel, _edge, _channelEventCallback):
        
        if _channel != None:
            event = Event(_edge, _channelEventCallback, _channel)
            _piBoardInstance.channelEvents[_channel] = event


class Event:

    eventCallback = None
    edge = None
    channel = None

    def __init__(self, _edge, _eventCallback, _channel):
        self.eventCallback = _eventCallback
        self.edge = _edge
        self.channel = _channel

   
class Service:
 
    serviceThreadCallback = None
 
    def __init__(self):
        print(self)
        
    def listen(self, _serviceThreadCallback):
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
                    _serviceThreadCallback(data)
                    
                else:
                    break         
    
    def setCallback(_serviceThreadCallback):
        global serviceThreadCallback
        serviceThreadCallback = _serviceThreadCallback

                
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

    def setPiBoardCallback(_serviceThread, _piBoardCallback):
        global piBoardCallback
        piBoardCallback = _piBoardCallback
         
    def threadify(self):
        global thread
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        

def ext_callback(_event):
    print "ext_callback"
    print _event.channel       
    print _event.edge       
    print _event.eventCallback

                
if __name__ == '__main__': 
     
    try:
        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.IN, 0, GPIO.PUD_UP)
            GPIO.add_event_detect(22, GPIO.FALLING, ext_callback, bouncetime=1500)
            time.sleep(1000)
    except KeyboardInterrupt:
        pass      
