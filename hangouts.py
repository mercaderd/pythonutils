#!/usr/bin/python
# -*- coding: utf-8 -*-
#Created on Tue Nov 25 20:09:51 2014

import xmpp, sys

class hangouts(object):
    def __init__(self,user,password):
        self.jid = xmpp.protocol.JID(user+'@gmail.com')
        self.cl=xmpp.Client(self.jid.getDomain(),debug=[])
        self.cl.connect()
        self.cl.auth(self.jid.getNode(),password)

    def sendmessage(self,destinatario,mensaje):
        if self.cl is not None:        
            self.cl.send(xmpp.protocol.Message(destinatario+'@gmail.com',mensaje, typ='chat'))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: hangouts user pass destinatario mensaje"
        sys.exit(1)
    h=hangouts(user=sys.argv[1], password=sys.argv[2])
    if h is not None:
        print h       
        h.sendmessage(destinatario=sys.argv[3],mensaje=sys.argv[4])
        