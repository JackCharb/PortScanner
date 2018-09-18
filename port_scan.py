#!/usr/bin/env python3

# Jack Charbonneau 10/14/2017

import argparse
import socket


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', type=str, dest='tgtHost', help='specify target host')
    parser.add_argument('-p', type=str, dest='tgtPorts', help='specify target ports separated by commas')

    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPorts = args.tgtPorts

    if (tgtHost is None):
        print(parser.usage)  # write parser usage
        exit(0)
    else:
        if tgtPorts is None:
            tgtPorts = list(range(1, 65536))
        else:
            tgtPorts = args.tgtPorts.split(",")
        portScan(tgtHost, tgtPorts)


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost)  # use get address info instead
    except socket.gaierror:
        print("[-] Could not resolve hostname: '%s'" % tgtHost)
        return
    except socket.error:
        print("[-] Could not connect to server")
        return

    try:
        tgtName = socket.gethostbyaddr(tgtIP) # fix this
        print("[-] Scan results for: " + tgtName[0])
    except:
        print("[-] Scan results for: " + tgtIP)

    socket.setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        connScan(tgtHost, int(tgtPort))


def connScan(tgtHost, tgtPort):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((tgtHost, tgtPort))
        print("[+] Port %d open" % tgtPort)
        sock.close()

    except KeyboardInterrupt:
        print()
        exit()

    except:
        print("[-] Port %d closed" % tgtPort)

if __name__ == "__main__":
    main()
