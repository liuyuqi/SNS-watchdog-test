# the main program of SNS-watchdog-test
# Linux only

from socket import *
import struct

class WatchdogInfo:
    'basic information of watchdog'
    watchdog_ipaddr = "" # in the form of string
    known_ip_addr_dict = {} # a dictionary containing all known ip addresses
    def __init__(self):
        print "\nWelcome to SNS watchdog! System initializing..."
        # gethostbyname(gethostname()) doesn't really work here...
        tmp_sock = socket(AF_INET, SOCK_DGRAM)
        tmp_sock.connect(("8.8.8.8", 0))
        print "local ip address is %s" % tmp_sock.getsockname()[0]
        
        self.known_ip_addr_dict = {}
        
    

class AddrRecord:
    '''a record entry in WatchDogInfo.known_ip_addr_dict
    (the 'value' part of the key-value pair in the dictionary)
    '''
    
    

def main():
    ''' the main procedure of the watchdog app.'''
    # init the watchdog
    watchDog = WatchdogInfo()
    
    try:
        s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
    except:
        print "Failed to open a socket!"
        return
    
    while True:
        pkt = s.recvfrom(65535)
        parse_pkt(pkt[0])


def parse_pkt(pkt_raw):
    ''' parses the packet.'''
    
    # Parsing the IP header...
    ip_header_raw = pkt_raw[0:20]
    ip_header = struct.unpack('!BBHHHBBH4s4s', ip_header_raw)
    ip_version_ihl = ip_header[0]
    ip_version = ip_version_ihl >> 4 # ip version is got.
    if ip_version == 4:
        ip_src_addr_strVal = inet_ntoa(ip_header[8]) # ip source addr is got.
        ip_dst_addr_strVal = inet_ntoa(ip_header[8]) # ip dest addr is got.
        print "Got a packet, src = %s (%s), dst = %s (%s)" % \
                (ip_src_addr_strVal, gethostbyaddr(ip_src_addr_strVal), \
                ip_dst_addr_strVal, gethostbyaddr(ip_dst_addr_strVal))
        
    
    

if __name__ == '__main__':
    main()
