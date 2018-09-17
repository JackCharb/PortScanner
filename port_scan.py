#!/usr/bin/env python3

# Jack Charbonneau 10/14/2017

import argparse
from socket import *

parser = argparse.ArgumentParser()

parser.add_argument('-H', type=str, dest='tgtHost', help='specify target host')
parser.add_argument('-p', type=str, dest='tgtPorts', help='specify target ports separated by commas')

args = parser.parse_args()
tgtHost = args.tgtHost
tgtPorts = args.tgtPorts

def main():
    if (tgtHost is None) | (tgtPorts[0] is None):
        print(parser.usage)
        exit(0)
    else:
        portScan(tgtHost, tgtPorts)


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(gtgHost) # use get address info instead
    except:
        print("[-] Cannot resolve '%s': Unknown Host" % tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("[-] Scan results for: " + tgtName[0])
    except:
        print("[-] Scan results for: " + tgtIP)

    setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        print("Scanning Port " + tgtPort)
        connScan(tgtHost, int(tgtPort))


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        print("[+] %d tcp open" % tgtPort)
        connSkt.close()

    except:
        print("[-] %d tcp closed" % tgtPort)

if __name__ == "__main__":
    main()
