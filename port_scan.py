#!/usr/bin/env python3

# Jack Charbonneau 09/17/2018

import argparse
import socket
import csv


def main():
    """Perform a port scan with the given target host and target ports. 
    If no target ports are given scan the 1000 most frequently used TCP ports.
    """
    #  Get target host and ports from command line arguments
    tgtHost, tgtPorts = parse()

    if tgtPorts is None:
        #  If no ports were provided, load in the top 1000 TCP ports.
        with open('default_ports.csv', newline='') as ports:
            reader = csv.reader(ports)
            tgtPorts = list(reader)[0]
    else:
        #  Use provided ports
        tgtPorts = tgtPorts.split(",")

    resolveHost(tgtHost, tgtPorts)
    scanPorts(tgtHost, tgtPorts)


def parse():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('-H', required=True, type=str, dest='tgtHost',
                        help='specify target host')
    parser.add_argument('-p', type=str, dest='tgtPorts',
                        help='specify target ports separated by commas')
    args = parser.parse_args()
    return (args.tgtHost, args.tgtPorts)


def resolveHost(tgtHost, tgtPorts):
    """Ensure that the given target host can be resolved
    to a valid hostname.
    """
    try:
        #  Get IP of provided host
        tgtIP = socket.gethostbyname(tgtHost)
    except socket.gaierror:
        print("[-] Could not resolve hostname: '%s'" % tgtHost)
        return
    except OSError:
        print("[-] Could not connect to server")
        return

    try:
        #  Get primary hostname from IP
        tgtName = socket.gethostbyaddr(tgtIP)
        print("[-] Scan results for: '%s'" % tgtName[0])
    except:
        print("[-] Scan results for: '%s'" % tgtIP)


def scanPorts(tgtHost, tgtPorts):
    """Scan each port in the list of target ports and print
    whether the port is open or closed.
    """
    #  Each port has one second to respond before timeout
    socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((tgtHost, int(tgtPort)))
            print("[+] Port %d open" % int(tgtPort))
            sock.close()

        #  Allow program termination with ^C
        except KeyboardInterrupt:
            print()
            exit()

        except:
            print("[-] Port %d closed" % int(tgtPort))

if __name__ == "__main__":
    main()
