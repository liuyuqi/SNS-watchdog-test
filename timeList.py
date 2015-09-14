# Implementations of timeLists of each website.

import watchdog
import collections
import threading


# A fast implementation for finding a time list by its name.
class TimeListDict:
    def __init__(self):
        self.d = {} # dictionary key = name, value = TimeList obj.
    
    def getList(self, name):
        ''' Returning the TimeList object by the given name.'''
        return self.d[name]
    
    def getAllLists(self):
        ''' Returning a list of all TimeList objects.'''
        return self.d.values()
    
    def addList(self, name, timeList):
        ''' Adding a new timeList to the dictionary. '''
        self.d[name] = timeList
        

class TimeList:
    def __init__(self, name):
        self.name = name # for example, "twitter"
        self.q = collections.deque() # the list body, containing timestamps.
        self.l = threading.Lock() # lock of the current time list.
        
    def push(self, timeStamp):
        ''' Push a timeStamp into the current queue. '''
        self.l.acquire()
        self.q.append(timeStamp)
        self.l.release()
    
    def pop(self):
        ''' Pop the oldest timeStamp from the current queue. '''
        self.l.acquire()
        ts = None
        if len(self.q) > 0:
            ts = self.q.popleft()
        self.l.release()
        return ts
    
