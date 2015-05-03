# test.py
# the main program of SNS-watchdog-test

import pcap, dpkt, time

def process(timestamp, pkt, undefined):
    '''When a TCP segment arrives,
        extracts and returns it's Src and Dst IP address.'''
    p = dpkt.ethernet.Ethernet(pkt)
    ip_src = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.src)))
    ip_dst = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
    print "*** Got TCP segment from %s to %s!" % (ip_src, ip_dst)

def init_capture():
    ''' Initializes the capture process '''
    pc = pcap.pcap(name = "wlp0s26u1u4i2", timeout_ms = 1000000000)
    pc.setfilter('tcp port 80')
    return pc

def main():
    print "Welcome\n"
    pc = init_capture()
    
    ret = pc.loop(0, process, None)
    if ret == None:
        print "Exited with return value 0"
    else:
        print "Exited with return value %d" % ret

if __name__ == '__main__':
    main()
