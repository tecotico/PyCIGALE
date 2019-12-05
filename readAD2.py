#!/usr/bin/env python


f = open("mask4.ad2", "rb")
try:
    byte = f.read(1)
    while byte != "":
        # Do stuff with byte.
        byte = f.read(1)
        print byte
finally:
    f.close()
