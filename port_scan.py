#!/usr/bin/env python3

# Jack Charbonneau 09/17/2018

import argparse
import socket


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', required=True, type=str, dest='tgtHost',
                        help='specify target host')
    parser.add_argument('-p', type=str, dest='tgtPorts',
                        help='specify target ports separated by commas')

    args = parser.parse_args()
    tgtHost = args.tgtHost  # are these needed?
    tgtPorts = args.tgtPorts

    if (tgtHost is None):
        parser.print_usage()
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
    except OSError:
        print("[-] Could not connect to server")
        return

    try:
        tgtName = socket.gethostbyaddr(tgtIP)  # fix this
        print("[-] Scan results for: " + tgtName[0])
    except:
        print("[-] Scan results for: " + tgtIP)

    socket.setdefaulttimeout(1)  # check this

    for tgtPort in tgtPorts:
        connScan(tgtHost, int(tgtPort))


def connScan(tgtHost, tgtPort):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # factor out
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
