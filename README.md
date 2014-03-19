pointicq
========

Private Point.IM to ICQ gateway.

Installing:

JID setup: register it, add ICQ/MRIM/AOL/etc transport with bot UIN/MRID/etc (if necessary), fill info, go http://point.im/profile/accounts, add this one, confirm it and logout from client.
- install python2 (I'm used 2.7.6), xmpppy (in Arch Linux) or python-xmpp (in Debian)
- put pointicq.conf to /etc/pointicq.conf and fill in JID, password and dedicated JID for recieving messages
- put pointicq.py wherever you want and do it executable (chmod +x pointicq.py)
- run pointicq.py

How to make it daemonize? Google knows, but I'm add "/usr/bin/python2.7 /usr/bin/local/pointicq.py &" in /etc/rc.local before "exit 0".

Usage: just add bot to your roster and use it as p@point.im.
