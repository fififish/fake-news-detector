import configparser

def readconfig(configFileName):
    config = configparser.ConfigParser() #create a config parser 
    config.read(configFileName)
    #format: n,f,hostip,baseportnum
    return (config['orderer']['replicas'],config['orderer']['f'],config['endorser']['host'],config['endorser']['baseport'])

#This routine writes a config value to a given .ini file
def writeconfig(configFileName, configSection, configName, configValue):
    config = configparser.ConfigParser() #create a config parser
    config.read(configFileName)

    config[configSection][configName] = configValue
    with open(configFileName, 'w') as configFile:
        config.write(configFile) 
    return 1

#This returns the name of the Python config file
def getPythonConfigName():
    pythonConfigName = "config.ini"
    return pythonConfigName

#This returns the location of the BFT-SMaRt library hosts.config file
def getBFTHostsConfigFileName():
    BFTHostsConfigName = "/home/hie-blockchain/test/hie_blockchain/library/config/hosts.config" #TO DO change the location of this
    return BFTHostsConfigName

#This returns the location of the BFT-SMaRt library hosts.config file
def getBFTHostsConfigFileName2():
    BFTHostsConfigName = "/home/hie-blockchain/test/hie_blockchain/config/hosts.config" #TO DO change the location of this
    return BFTHostsConfigName

#Returns the name of the file with the header info in it about the authors and the license
def getHostsConfigHeaderFileName():
    headerFileName = "hostsHeader.txt"  #file name
    return headerFileName

#Gets the disclaimer info to include in the top of the hosts.config file.  This disclaimer info is the
#    Apache license, author names, etc.  
def getHostsConfigHeader():
    #read the java config file from BFT-SMaRt
    try:
        hostsConfigHeaderFile = getHostsConfigHeaderFileName()  #Get the file name where the authors and license info is.
        configHeader = []
        with open(hostsConfigHeaderFile, "r") as headerFile:
            for line in headerFile:
                configHeader.append(line)            

    finally:
        headerFile.close()   #close the file

    return configHeader

def getReplicaCount():
    config = configparser.ConfigParser() #create a config parser 
    config.read(getPythonConfigName())
    #format: n,f,hostip,baseportnum
    return (config['orderer']['replicas'])


#extracts a value from the config.ini file, for the section given
def ConfigSectionMap(section):

    #Open up the python config file:
    config = configparser.ConfigParser() #create a config parser 
    config.read(getPythonConfigName())    #read the config file

    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip:  %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


#This function takes a config entry from config.ini and builds a line for the hosts.config file
#config.ini entry:
#  [host0]
#  replica_id = 0 
#  ip_address = 127.0.0.1
#  port_number = 11000
#Becomes hosts.config entry:
# 0 127.0.0.1 11000 
#parameter replicaName should be host0, or host1, or hostn
def getHostConfigLine(replicaName):

    replica_id  = ConfigSectionMap(replicaName)['replica_id']  #Get the replica id for the given replica
    ip_address  = ConfigSectionMap(replicaName)['ip_address']  #Get the IP address for the given replica
    port_number = ConfigSectionMap(replicaName)['port_number'] #Get the port number for the given replica
    hostsConfigLine = replica_id + " " + ip_address + " " + port_number
    #print hostsConfigLine
    return hostsConfigLine

#For a given number "n" of replicas, read the config.ini file and build a hosts.config line.  Concatenate those hosts.config lines 
#   into an entire section.  The section will have all the host entries needed for hosts.config file.
def getHostsConfigSection():
    numberOfHosts = getReplicaCount() #number of hosts to get
    print "DEBUG number of hosts is: " + str(numberOfHosts)
    cnt = 0
    getHostsConfigSection =range(int(numberOfHosts))
    while cnt < int(numberOfHosts):               #loop while we are less than the given number of replicas.
        replicaName = "host" + str(cnt)           #build "host0" , "host1", "hostn"
        line = getHostConfigLine(replicaName)     #get the java hosts.config line
        getHostsConfigSection[cnt] = line         #add the line to an array
        #print line
        cnt +=1                                   #increment the counter
    return getHostsConfigSection            
    

#Copies the config.ini file to the hosts.config file
def syncConfigFiles():
    bftSmartHostsConfigFileName = getBFTHostsConfigFileName()
    bftSmartHostsConfigFileName2 = getBFTHostsConfigFileName2() #temporary hack until we determine which config directory to retain
    #read the java config file from BFT-SMaRt

    
    try:
        header = getHostsConfigHeader()
        hosts  = getHostsConfigSection()
        with open(bftSmartHostsConfigFileName, "w") as bftHostsConfig:
            for line in header:
                bftHostsConfig.write(line)
            for line in hosts:
                bftHostsConfig.write("\n" + line ) #Issue #6.  Header needs a new line

        with open(bftSmartHostsConfigFileName2, "w") as bftHostsConfig:
            for line in header:
                bftHostsConfig.write(line)
            for line in hosts:
                bftHostsConfig.write("\n" + line ) #Issue #6.  Header needs a new line





    finally:
        bftHostsConfig.close()   #close the file

    #format: n,f,hostip,baseportnum
    return 1