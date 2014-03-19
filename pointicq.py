#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys, os, signal, time
import xmpp, ConfigParser

def iqCB(conn,iq_node):
    reply=iq_node.buildReply('result')
    conn.send(reply)

def messageCB(conn,msg):
    global pointicqsourcejid
    if (msg.getFrom() == pointicqsourcejid):
        conn.send(xmpp.Message('p@point.im',msg.getBody()))
    if (msg.getFrom() == 'p@point.im/point'):
        conn.send(xmpp.Message(pointicqsourcejid,msg.getBody()))

def presenceCB(conn,msg):
    global pointicqsourcejid
    if ( msg.getType() == "subscribe" and msg.getFrom() == pointicqsourcejid):
        conn.send(xmpp.Presence(to=msg.getFrom(), typ='subscribed'))
        conn.send(xmpp.Presence(to=msg.getFrom(), typ='subscribe'))
    
def StepOn(conn):
    global pointicqbotlastping
    if time.time() - pointicqbotlastping > 30:
        pointicqbotlastping = time.time()
        ping = xmpp.Protocol('iq',typ='get',payload=[xmpp.Node('ping',attrs={'xmlns':'urn:xmpp:ping'})])
        res = conn.SendAndWaitForResponse(ping, 1)
    try:
        conn.Process(1)
    except KeyboardInterrupt:
        return 0
    return 1
    
def GoOn(conn):
    while StepOn(conn): pass
    conn.disconnect()
        
def main():
    config = ConfigParser.ConfigParser()
    config.read('/etc/pointicq.conf')
    user=(config.get('account', 'login'))
    password=(config.get('account', 'password'))
    presence=(config.get('presence','presence'))
    global pointicqsourcejid
    pointicqsourcejid=(config.get('sources','jid'))
    jid=xmpp.protocol.JID(user)
    # cl = xmpp.Client(jid.getDomain()) # enable debug
    cl = xmpp.Client(jid.getDomain(), debug=[]) # disable debug
    if cl.connect() == "":
        print "not connected"
        sys.exit(0)
    if cl.auth(jid.getNode(),password,"Point ICQ bot") is None:
        print "authentication failed"
        sys.exit(0)
    cl.UnregisterDisconnectHandler(cl.DisconnectHandler)
    cl.RegisterDisconnectHandler(cl.reconnectAndReauth())
    cl.RegisterHandler('presence', presenceCB)
    cl.RegisterHandler('iq',iqCB)
    cl.RegisterHandler('message', messageCB)
    cl.sendInitPresence()
    GoOn(cl)

pointicqsourcejid = ''
pointicqbotlastping = time.time()    
main()
