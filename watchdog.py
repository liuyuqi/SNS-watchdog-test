# the main program of SNS-watchdog-test
# Linux only

from socket import *
import struct
import configFile
import timeList
import analyzer

class WatchdogInfo:
    '''basic information of watchdog'''
    
    local_ipaddr = "" # in the form of string
    
    known_ip_addr_dict = {} # a dictionary containing all known ip addresses
    
    monitor_list = [] # a list containing all the hostnames to monitor
    
    timeListDict = None # a dictionary containing all timeLists.
    
    def __init__(self):
        
        print "\nWelcome to SNS watchdog! System initializing..."
        # gethostbyname(gethostname()) doesn't really work here...
        
        # initializing the sockets.
        tmp_sock = socket(AF_INET, SOCK_DGRAM)
        tmp_sock.connect(("8.8.8.8", 0))
        self.local_ipaddr = tmp_sock.getsockname()[0]
        print "local ip address is %s\n" % self.local_ipaddr
        
        # Reading the configuration file.
        self.known_ip_addr_dict = {}
        self.monitor_list = []
        configFile.parseConfigFile("config-watchdog.conf", self.monitor_list);
        
        # initializing the time lists.
        timeListDict = timeList.TimeListDict()
        for mEntry in self.monitor_list:
            newTimeList = timeList.TimeList(mEntry.displayName)
            timeListDict.addList(mEntry.displayName, newTimeList)
        
            
     
        

# Alert: this is a list, not set. Efficiency is low.
class MonitorEntry:
    '''a record entry in WatchDogInfo.monitor_list'''
    displayName = ""
    filterName = ""
    def __init__(self, dName, fName):
        self.displayName = dName
        self.filterName = fName
    

# Alert: this is not used yet, efficiency is low.
class KnownIpEntry:
    '''a record entry in WatchDogInfo.known_ip_addr_dict
    (the 'value' part of the key-value pair in the dictionary)
    '''
    ip_addr_str = ""
    host_name = ""
    display_name = ""
    def __init__(self, ip, hname, dname):
        self.ip_addr_str = ip
        self.host_name = hname
        self.display_name = dname
    

def main():
    ''' the main procedure of the watchdog app.'''
    # init the watchdog
    watchDog = WatchdogInfo()
    
    try:
        s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
    except:
        print "Failed to open a socket!"
        print "Did you grant Administrator permisson to me?"
        return
    
    while True:
        pkt = s.recvfrom(65535)
        parse_pkt(watchDog, pkt[0])


def parse_pkt(watchDog, pkt_raw):
    ''' parses the packet.'''
    
    # Parsing the IP header...
    ip_header_raw = pkt_raw[0:20]
    ip_header = struct.unpack('!BBHHHBBH4s4s', ip_header_raw)
    ip_version_ihl = ip_header[0]
    ip_version = ip_version_ihl >> 4 # ip version is got.
    
    if ip_version == 4:
        
        ip_src_addr_strVal = inet_ntoa(ip_header[8]) # ip source addr is got.
        ip_dst_addr_strVal = inet_ntoa(ip_header[9]) # ip dest addr is got.
        src_dname = ""
        dst_dname = ""
        
        try:
            src_dname = gethostbyaddr(ip_src_addr_strVal)[0]
        except:
            src_dname = "cannot.get.such.host"
        
        if ip_dst_addr_strVal != watchDog.local_ipaddr:
            print "This is not right... dest addr is not local"
        else:
            dst_dname = "localhost"
            
        print "Got a packet, src = %s (%s), dst = %s (%s)" % \
                (ip_src_addr_strVal, src_dname, \
                ip_dst_addr_strVal, dst_dname)
                
        # issuing an alert
        for monitorEntry in watchDog.monitor_list:
            #print "debug: monitor entry is %s" % monitorEntry.filterName
            if monitorEntry.filterName in src_dname:
                print "\n*****ALERT: You're visiting %s page!" % monitorEntry.displayName
                break
        
    
    

if __name__ == '__main__':
    main()
