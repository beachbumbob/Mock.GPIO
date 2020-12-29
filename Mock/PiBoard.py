import GPIO

class Board:
    channelConfigs= {}
    channelEvents= {}
    __instance = None
    
#     class Event:
#         def __init__(self,edge, callback):
#             self.edge = edge
#             self.callback = callback 

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Board.__instance == None:
            Board()
        return Board.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Board.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Board.__instance = self
    
    def setChannelConfig(self,channel):
        if channel != None:
            self.channelConfigs[channel.chanel] = channel
        
    def setChannelEvent(self,channel,edge,callback):
        if channel != None:
            self.channelEvents[channel] = Event.Event(edge,callback)
        
   
   
class Event(object):
    '''
    classdocs
    '''

    def __init__(self,edge, callback):
        '''
        Constructor
        '''
        self.edge = edge
        self.callback = callback 
 
   
class service(object):
    '''
    classdocs
    '''
    global callback
 
    def __init__(self):
        '''
        Constructor
        '''
#         self.callback = callback
      
    def listen(self,callback):
#     def listen(self):
#     def listen():
        self.callback = callback
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
                    current_connection.sendall(data)
#                     print data
                    cm = self.callback
                    cm(data) 
                else:
                    break         
    
    def setCallback(self,callback):
        self.callback  = callback
        
    def getCallback(self):
       return self.callback
        
        
class ServiceThread(object):

    global callback

    def __init__(self, interval=1):
        self.interval = interval

    def run(self):

#         while True:
            svc = S.service()
            svc.listen(self.callback)

#         while True:
#             cm = self.getCallback()
#             cm(self)
#             print('Doing something imporant in the background')
#             time.sleep(self.interval)

    def setCallback(self, callback):
        self.callback = callback
 
    def getCallback(self):
        return self.callback
        
    def threadify(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        
        
def ext_callback(val):
    print "ext_callback"
    print val        
        
        
                
# def handler(pin):
#     print pin
#          
# if __name__ == '__main__':
#     
#     
# #GPIO.setmode(GPIO.BCM)
# #GPIO.setup([redButton, blueButton], GPIO.IN, pull_up_down=GPIO.PUD_UP)   
# 
#     
#     
#     try:
#          
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(22, GPIO.IN, 0, GPIO.PUD_UP)
#         GPIO.add_event_detect(22, GPIO.FALLING, handler, bouncetime=1500)
#     except KeyboardInterrupt:
#         pass      
