import yaml


def readconfig():
    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    #format: n,f,hostip,baseportnum

    return (cfg['orderer']['replicas'],cfg['orderer']['f'],cfg['endorser']['host'],cfg['endorser']['baseport'])
