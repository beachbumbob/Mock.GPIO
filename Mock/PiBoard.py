import GPIO as GPIO
import threading
import time
import socket as sk

class Board():
    channelConfigs = {}
    channelEvents = {}
    __instance = None
    global serviceThread
    global piBoardCallback
    
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
            self.serviceThread = ServiceThread()
            self.serviceThread.piBoardCallback = piBoardCallback
#             self.serviceThread.setPiBoardCallback(piBoardCallback)
            self.serviceThread.threadify()
            
            Board.__instance = self
            
           
    def piBoardCallback(self,val):
        print "piBoardCallback"
        # This assumes that val is in format {channel:[HI|LOW]}
        x = val.split(":")
        print(val)
        channel = x[0]
        edge = x[1]
        print(channel)
        print(edge)
        event = self.channelEvents[channel]
        print(event)
#         event.getCallback(x[1])
    
    def setChannelConfig(self, channel):
        if channel != None:
            self.channelConfigs[channel.chanel] = channel
        
    def setChannelEvent(self, channel, edge, eventCallback):
        if channel != None:
            event = Event(edge,eventCallback)
            self.channelEvents[channel] = Event(edge,eventCallback)
#             self.channelEvents[channel].setEventCallback = eventCallback
   
# class Event(object):
class Event:
    '''
    classdocs
    '''

    global eventCallback
    global edge

    def __init__(self,edge,eventCallback):
        '''
        Constructor
        '''
        self.edge = edge
        self.eventCallback = eventCallback 
    
    def getEventCallback():
        return self.eventCallback
   
    def setEventCallback(eventCallback):
        self.eventCallback = eventCallback
   
# class Service(object):
class Service:

    global serviceThreadCallback
 
    def __init__(self):
        print "Service __init__"
        
    def listen(self,serviceThreadCallback):
        self.serviceThreadCallback = serviceThreadCallback
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
#                     current_connection.sendall(data)
                    self.serviceThreadCallback(data)
                    
                else:
                    break         
    
    def setCallback(self, serviceThreadCallback):
        self.serviceThreadCallback = serviceThreadCallback
        
    def getCallback(serviceThreadCallback):
       return self.serviceThreadCallback
        
class ServiceThread:

    global piBoardCallback
    global thread
    global svc

    def __init__(self, interval=1):
        self.interval = interval

    def run(self):
            self.svc = Service()
            self.svc.listen(self.piBoardCallback)

    def setPiBoardCallback(piBoardCallback):
        self.piBoardCallback = piBoardCallback
 
    def getPiBoardCallback():
        return self.piBoardCallback
        
    def threadify(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()  # Start the execution
        
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
