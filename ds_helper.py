#!/usr/bin/env python2.6
# -*- coding: utf-8
import re
from threading import Lock, RLock


print_message_format = "> {0}< : {1}"


class RE:
    FLAGS = re.IGNORECASE
    FILE_DATE_STRING = r'\b\d\d\/\d\d\/\d\d\d\d\b'
    FILE_TIME_STRING = r'\b\d\d:\d\d[ap]\b'
    FILE_SIZE_PREAMBLE = FILE_DATE_STRING + r'\s+?' + FILE_TIME_STRING + r'\s+?(\d+?)\s+?'
    PRIMARY_BOF_IMAGE = re.compile(r'primary-image\s+?(\S+)\b', FLAGS)
    SECONDARY_BOF_IMAGE = re.compile(r'secondary-image\s+?(\S+)\b', FLAGS)
    FILE_DATE = re.compile(FILE_DATE_STRING)
    FILE_TIME = re.compile(FILE_TIME_STRING)
    DIR_FILE_PREAMBLE = re.compile(FILE_DATE_STRING+r'\s+?'+FILE_TIME_STRING+r'\s+?(?:<DIR>|\d+?)\s+?', FLAGS)
    DS_TYPE = re.compile(r'\bSAS-[XM]\b', FLAGS)
    '''
    TiMOS-B-4.0.R2
    TiMOS-B-5.0.R2
    TiMOS-B-7.0.R9
    TiMOS-B-7.0.R13
    '''
    SW_VERSION = re.compile(r'TiMOS-\w-\d\.\d\.R\d+?\b', FLAGS)
    FREE_SPACE_SIZE = re.compile(r'\b(\d+?)\s+?bytes free\.', FLAGS)
    DS_NAME = re.compile(r'\bds\d-[0-9a-z]+\b', FLAGS)


class COLORS:

    class STYLE:
        normal    = 0
        highlight = 1
        underline = 4
        blink     = 5
        negative  = 7

    class FOREGROUND:
        black   = 30
        red     = 31
        green   = 32
        yellow  = 33
        blue    = 34
        magenta = 35
        cyan    = 36
        white   = 37

    class BACKGROUND:
        black   = 40
        red     = 41
        green   = 42
        yellow  = 43
        blue    = 44
        magenta = 45
        cyan    = 46
        white   = 47

    end = "\x1b[0m"
    colored = '\x1b[{style};{foreground};{background}m'

    black   = colored.format(style=STYLE.normal, foreground=FOREGROUND.black  , background=BACKGROUND.white)
    red     = colored.format(style=STYLE.normal, foreground=FOREGROUND.red    , background=BACKGROUND.black)
    green   = colored.format(style=STYLE.normal, foreground=FOREGROUND.green  , background=BACKGROUND.black)
    yellow  = colored.format(style=STYLE.normal, foreground=FOREGROUND.yellow , background=BACKGROUND.black)
    blue    = colored.format(style=STYLE.normal, foreground=FOREGROUND.blue   , background=BACKGROUND.black)
    magenta = colored.format(style=STYLE.normal, foreground=FOREGROUND.magenta, background=BACKGROUND.black)
    cyan    = colored.format(style=STYLE.normal, foreground=FOREGROUND.cyan   , background=BACKGROUND.black)
    white   = colored.format(style=STYLE.normal, foreground=FOREGROUND.white  , background=BACKGROUND.black)

    colors = [white,
              cyan,
              green,
              colored.format(style=STYLE.normal, foreground=FOREGROUND.blue, background=BACKGROUND.cyan),
              yellow,
              colored.format(style=STYLE.normal, foreground=FOREGROUND.blue, background=BACKGROUND.green),
              magenta,
              colored.format(style=STYLE.normal, foreground=FOREGROUND.cyan, background=BACKGROUND.blue),
              black,
              colored.format(style=STYLE.normal, foreground=FOREGROUND.blue, background=BACKGROUND.yellow),
              ]

    warning = yellow
    fatal = colored.format(style=STYLE.highlight, foreground=FOREGROUND.red, background=BACKGROUND.black)
    error = red
    ok = green
    info = cyan


__ds_host_name_parse = re.compile(r'\b([A-Z]+?\d+?-[A-Z]{3})(\d+?)\b', re.IGNORECASE)


def extract(regexp, text):
    """

    :param regexp: regular expression
    :param text: source for extracting
    :param flags: default re.IGNORECASE Only for string regexp arguments
    :return: first occur regular expression
    """
    try:
        return re.findall(regexp,text).pop()
    except IndexError as error:
        return None
    return


def is_contains(regexp, text):
    """

    :param regexp:
    :param text:
    :param flags: default re.IGNORECASE Only for string regexp arguments
    :return: True if string contains regular expression
    """
    if re.search(regexp,text):
        return True
    else:
        return False


def ds_print(host, message, print_lock=None, log_file_name=None, host_color=None, message_color=None):
    """

    :param host:
    :type host: str
    :param message:
    :type message: str
    :param print_lock: io lock object
    :type print_lock: object Lock
    :param log_file_name: 
    :type log_file_name: str
    :param host_color: 
    :type host_color: COLORS
    :param message_color: 
    :type message_color: COLORS
    :return: None
    :rtype: None
    """

    from threading import Lock
    if __ds_host_name_parse.findall(host):
        site_preamble, site_number = __ds_host_name_parse.findall(host)[0]
        host = "{0}{1:<4d}".format(site_preamble, int(site_number))

    if host_color and message_color:
        colored_host = host_color + host + COLORS.end
        colored_message = message_color + message + COLORS.end
    elif host_color:
        colored_host = host_color + host + COLORS.end
        colored_message = host_color + message + COLORS.end
    elif message_color:
        colored_host = host
        colored_message = message_color + message + COLORS.end
    else:
        colored_host = host
        colored_message = message

    if print_lock:
        try:
            print_lock.acquire()
        except:
            pass

    print print_message_format.format(colored_host, colored_message)

    if print_lock:
        try:
            print_lock.release()
        except:
            pass
    if log_file_name:
        try:
            with open(log_file_name, 'a') as log_file:
                log_file.write("{0}\n".format(message))
                log_file.close()
        except IOError:
            pass


if __name__ == "__main__":

    sample_text = r"""A:ds3-kha3# show version
TiMOS-B-7.0.R9 both/mpc ALCATEL SAS-M 7210 Copyright (c) 2000-2015 Alcatel-Lucent.
All rights reserved. All use subject to applicable license agreements.
Built on Thu Oct 15 08:11:18 IST 2015 by builder in /home/builder/7.0B1/R9/panos/main
A:ds3-kha3# shov [1D [1D[1D [1Dwp[1D [1D bof
===============================================================================
BOF (Memory)
===============================================================================
    primary-image      cf1:\images\TiMOS-7.0.R9\both.tim
    secondary-image    cf1:\images\TiMOS-B-4.0.R2\both.tim
    primary-config     cf1:\ds3-kha3.cfg
#eth-mgmt Port Settings:
    no  eth-mgmt-disabled
    eth-mgmt-address   10.50.70.46/24 active
    eth-mgmt-route     10.44.1.219/32 next-hop 10.50.70.1
    eth-mgmt-autoneg
    eth-mgmt-duplex    full
    eth-mgmt-speed     100
#uplinkA Port Settings:
    uplinkA-port       1/1/7
    uplinkA-autoneg
    uplinkA-duplex     full
    uplinkA-speed      1000
    uplinkA-address    0
    uplinkA-vlan       0
#uplinkB Port Settings:
    uplinkB-port       1/1/2
    uplinkB-autoneg
    uplinkB-duplex     full
    uplinkB-speed      1000
    uplinkB-address    0
    uplinkB-vlan       0
#System Settings:
    wait               3
    persist            on
    console-speed      115200
    uplink-mode        network
    use-expansion-card-type   m2-xfp
    no  console-disabled
===============================================================================
A:ds3-kha3# file version cf1:\images\TiMOS-7.0.R9\both.tim
TiMOS-B-7.0.R9 for 7210 SAS-M
Thu Oct 15 08:11:18 IST 2015 by builder in /home/builder/7.0B1/R9/panos/main
A:ds3-kha3# file version boot.tim
TiMOS-L-4.0.R2 for 7210 SAS-M
Mon Oct 31 16:19:31 IST 2011 by builder in /builder/4.0B1/R2/panos/main
A:ds3-kha3# file dit [1D [1D[1D [1Dr boot.tim


Volume in drive cf1 on slot A is /flash.

Volume in drive cf1 on slot A is formatted as FAT16

Directory of cf1:

03/19/2012  12:05p             4235928 boot.tim
               1 File(s)                4235928 bytes.

               0 Dir(s)                27013120 bytes free.

A:ds3-kha3# g[1D [1Dfile dir cf1:\images\TiMOS-7.0.R9\both.tim


Volume in drive cf1 on slot A is /flash.

Volume in drive cf1 on slot A is formatted as FAT16

Directory of cf1:\images\TiMOS-7.0.R9

01/21/2001  01:51p            43352608 both.tim
               1 File(s)               43352608 bytes.

               0 Dir(s)                27013120 bytes free.


A:ds3-kha3# logout"""
    print RE.DS_NAME.findall(sample_text)
    print RE.DS_TYPE.findall(sample_text)
    print RE.PRIMARY_BOF_IMAGE.findall(sample_text)
    print RE.SECONDARY_BOF_IMAGE.findall(sample_text)
    print RE.DIR_FILE_PREAMBLE.findall(sample_text)
    print extract(RE.FILE_SIZE_PREAMBLE, sample_text)
    print RE.FREE_SPACE_SIZE.findall(sample_text)
    print RE.SW_VERSION.findall(sample_text)

    ds_print('none', 'Test: ', Lock())
    ds_print('none', 'Test: ', RLock())
    ds_print('none', 'Test: None')
