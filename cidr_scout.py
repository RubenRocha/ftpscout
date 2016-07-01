#!/usr/bin/env python3
import sys
import netaddr
import random

def main():
    if len(sys.argv) < 2:
        print("usage: ./cidr-scout.py 127.0.0.1/24")
        sys.exit(1)
    for sub in sys.argv[1:]:
        try:
            subnet_ips = netaddr.IPNetwork(sub)
            ip_list = list(subnet_ips)
            for ip in ip_list:
                print("{}".format(ip))
        except netaddr.core.AddrFormatError:
            pass

if __name__ == "__main__":
	main()
