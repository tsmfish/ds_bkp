#!/usr/bin/env python2.6
# -*- coding: utf-8

import sys
import threading
import time
import re
import getpass
import os
import optparse

sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/ecdsa-0.13-py2.6.egg/')
sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/requests-2.9.1-py2.6.egg')
sys.path.insert(1, '/home/erkki/.local/lib/python2.6/site-packages/paramiko-1.16.0-py2.6.egg')

import paramiko
from paramiko import AuthenticationException
from socket import gaierror
from scp import SCPClient
from ds_helper import ds_print, RE, extract

AUTHORISE_TRY_COUNT, \
CONNECT_TRY_INTERVAL = 5, 7


class OpenSSHException(BaseException):
    def __init__(self, *args, **kvargs):
        super(args, kvargs)


def get_file_name(ds, user, secret):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for k in range(AUTHORISE_TRY_COUNT):
        try:
            client.connect(hostname=ds, username=user, password=secret, port=22, look_for_keys=False, allow_agent=False)
            break
        except AuthenticationException as e:
            ds_print(ds, "Error while authorize: "+ str(e))
        except OpenSSHException as e:
            raise OpenSSHException(str(e))
        except Exception as e:
            ds_print(ds, e)
        time.sleep(CONNECT_TRY_INTERVAL)
    else:
        ds_print(ds, "Can`t authorize")
        raise OpenSSHException("Can`t authorize on " + ds)

    ds_print(ds, "*** SSH establish with ")
    channel = client.invoke_shell()

    channel.send("\n")
    channel.send("show bof\n \n \n \n")
    channel.send("logout\n")
    time.sleep(2)

    printout = ''
    while channel.recv_ready():
        printout += channel.recv(1024)
        time.sleep(0.2)

    client.close()

    prim_conf = re.findall(r'primary-config.*', printout).pop()
    res = re.findall(r'cf1:.*cfg', prim_conf).pop()
    ds_print(ds, '*** Config file name ' + res)
    return res


def get_file(ds, user, secret, name, file_name):
    dest = name + file_name
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for k in range(AUTHORISE_TRY_COUNT):
        try:
            client.connect(ds, 22, user, secret)
            break
        except OpenSSHException as e:
            raise OpenSSHException(str(e))
        except AuthenticationException as e:
            ds_print(ds, "Error while authorize: " + str(e))
        except Exception as e:
            ds_print(ds, "Error:: " + str(e))
        time.sleep(CONNECT_TRY_INTERVAL)
    else:
        ds_print(ds, "Can`t authorize")
        raise OpenSSHException("Can`t authorize on " + ds)

    ds_print(ds, "*** SCP connect establish ")
    scp = SCPClient(client.get_transport())
    ds_print(ds, '*** Get file ' + file_name + ' from ' + ds)
    scp.get(file_name, dest)

    return dest


def mv_to_140(ds, config):
    remote_dir = '/mnt/om_kie/Backups/DS/' + ds + '/' + time.strftime("%Y") + '/'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for k in range(AUTHORISE_TRY_COUNT):
        try:
            ssh.connect('10.44.4.28', username='smdmud\\stscheck_script',  key_filename='/home/butko/script/ds_bkp/.id_script_dsa')
            break
        except AuthenticationException as e:
            ds_print(ds, "Error while authorize: " + str(e))
        except OpenSSHException as e:
            raise OpenSSHException(str(e))
        except Exception as e:
            ds_print(ds, e)

        time.sleep(CONNECT_TRY_INTERVAL)
    else:
        ds_print(ds, "Can`t authorize")
        raise OpenSSHException("Can`t authorize on " + ds)
    scp = SCPClient(ssh.get_transport())
    ds_print(ds, '*** Move file ' + config + ' to ' + remote_dir)
    scp.put(config, remote_dir)
    os.remove(config)


def copy_ds_backup(DS, user, secret, name):
    try:
        mv_to_140(DS, get_file(DS, user, secret, name, get_file_name(DS, user, secret).replace('cf1:\\', '')))
    except gaierror:
        ds_print(DS, '!!! Does not exist')
    except BaseException as e:
        ds_print(DS, 'Error wile backup: ' + str(e))


parser = optparse.OptionParser(description='Get config from DS\'s and move them to 1.140',
                               usage="usage: %prog [file with ds list]")
parser.add_option("-f", "--file", dest="ds_list_file_name",
                  help="file with list DS", metavar="FILE")
#parser.add_option( help='Path to file with list of ds', required=True)

(options, args) = parser.parse_args()
if not options.ds_list_file_name and not args:
    parser.error("Use [-f <ds list file> | ds ds ds ...]")

ds_list = args
if options.ds_list_file_name:
    try:
        with open(options.ds_list_file_name) as ds_list_file:
            for line in ds_list_file.readlines():
                ds_list.append(extract(RE.DS_NAME, line))
    except IOError as e:
        print "Error while open file: {file}".format(file=options.ds_list_file_name)
        print e.message

if len(ds_list) < 1:
    print "No ds found in arguments."
    exit()

user = getpass.getuser()
secret = getpass.getpass('Password for DS:')

while True:
    st = raw_input("Enter a for \"After\" or b for \"Before\"\n: ").lower()
    if st == 'a' or st == 'b':
        break

name = time.strftime("%y%m%d_") + st + '_upgrade_'

#paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

print "Start running: {time}".format(time=time.strftime("%H:%m"))
if len(ds_list) == 1:
    copy_ds_backup(ds_list[0], user, secret, name)
else:
    threads = list()
    for ds in ds_list:
        try:
            thread = threading.Thread(target=copy_ds_backup, name=ds, args=(ds, user, secret, name))
            thread.start()
            threads.append(thread)
        except OpenSSHException as e:
            print ds_print(ds, str(e))

    for thread in threads:
        thread.join()

print "Finish running: {time}".format(time=time.strftime("%H:%m"))
