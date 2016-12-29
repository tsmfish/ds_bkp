#!/usr/bin/env python2.6
# -*- coding: utf-8
import base64
import sys
import logging



sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/ecdsa-0.13-py2.6.egg/')
sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/requests-2.9.1-py2.6.egg')
sys.path.insert(1, '/home/butko/.local/lib/python2.6/site-packages/netmiko-1.1.0-py2.6.egg/')
sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/paramiko-1.16.0-py2.6.egg')
sys.path.insert(1, '/home/butko/.local/lib/python2.6/site-packages/scp-0.10.2-py2.6.egg/')

from netmiko.alcatel.alcatel_sros_ssh import AlcatelSrosSSH
import paramiko
from scp import SCPClient

logging.basicConfig(level=logging.INFO)

client_paramiko = paramiko.SSHClient()
client_paramiko.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print "="*20 + " -netmiko- " + "="*20
print 'Normal connect - start'
try:
    client_netmiko = AlcatelSrosSSH(host='ds4-kha3',
                                    port=22,
                                    username='pmalko',
                                    password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'),
                                    secret=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Normal connect  - end\n\n'

print 'Unknown host - start'
try:
    client_netmiko = AlcatelSrosSSH(host='ds11-kha3',
                                    port=22,
                                    username='pmalko',
                                    password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'),
                                    secret=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Unknown host - end\n\n'

print 'Bad user - start'
try:
    client_netmiko = AlcatelSrosSSH(host='ds4-kha3',
                                    port=22,
                                    username='malko',
                                    password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'),
                                    secret=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Bad user - end\n\n'

print 'Bad password - start'
try:
    client_netmiko = AlcatelSrosSSH(host='ds4-kha3',
                                    port=22,
                                    username='pmalko',
                                    password=base64.b64decode(b'bm9uZQ==').decode('ascii'),
                                    secret=base64.b64decode(b'bm9uZQ==').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Bad password - end\n\n'

print "="*20 + " -paramiko- " + "="*20

print 'Normal connect - start'
try:
    client_paramiko.connect(hostname='ds2-kha3',
                            port=22,
                            username='pmalko',
                            password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e

print 'Unknown host - start'
try:
    client_paramiko.connect(hostname='ds21-kha3',
                            port=22,
                            username='pmalko',
                            password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Unknown host - end'

print 'Bad user - start'
try:
    client_paramiko.connect(hostname='ds2-kha3',
                            port=22,
                            username='malko',
                            password=base64.b64decode(b'a1A2Qy1ONmQ=').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Bad user - end'

print 'Bad password - start'
try:
    client_paramiko.connect(hostname='ds2-kha3',
                            port=22,
                            username='pmalko',
                            password=base64.b64decode(b'bm9uZQ==').decode('ascii'))
except BaseException as e:
    print "Exception Class Name: " + e.__class__.__name__
    print e
print 'Bad password - end'

scp = SCPClient(client_paramiko.get_transport())
