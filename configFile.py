# configFile.py
# contains code on reading and parsing the configuration file.
import watchdog

def parseConfigFile(fileName, monitor_list):
    ''' Reads the configuration file and updates the monitor list.
    '''
    configFile = open(fileName, "r")
    lineNumber = 0
    
    for line in configFile:
        
        lineNumber += 1
        
        if line.strip() == "" or line.strip()[0] == '#':
            continue
            
        cleanLine = line.strip()
        args = cleanLine.split(":")
        if len(args) != 2:
            print "Syntax error at %s, line %d: %s" % (fileName, lineNumber, line)
            continue
        else:
            displayName = args[0].strip()
            filterName = args[1].strip()
            if displayName == "" or filterName == "":
                print "Syntax error at %s, line %d: %s" % (fileName, lineNumber, line)
                continue
            else:
                newEntry = watchdog.MonitorEntry(displayName, filterName)
                monitor_list.append(newEntry)
    
    #for item in monitor_list:
        #print "%s,%s." % (item.displayName, item.filterName)
        
    configFile.close()
        
