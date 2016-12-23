#!/usr/bin/env python2.6
# -*- coding: utf-8
import re
import threading


class RE:
    FLAGS = re.IGNORECASE
    FILE_DATE_STRING = r'\b\d\d\/\d\d\/\d\d\d\d\b'
    FILE_TIME_STRING = r'\b\d\d:\d\d[am]\b'
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


def extract(regexp, text, flags=re.IGNORECASE):
    """

    :param regexp: regular expression
    :param text: source for extracting
    :param flags: default re.IGNORECASE Only for string regexp arguments
    :return: first occur regular expression
    """
    try:
        if regexp.__class__.__name__ == 'SRE_Pattern':
            return regexp.findall(text)[0]
        elif regexp.__class__.__name__ == str.__class__.__name__:
            return re.findall(regexp, text, flags)[0]
        else:
            return None
    except IndexError as error:
        return None


def is_contains(regexp, text, flags=re.IGNORECASE):
    """

    :param regexp:
    :param text:
    :param flags: default re.IGNORECASE Only for string regexp arguments
    :return: True if string contains regular expression
    """
    assert(regexp.__class__.__name__ not in ('SRE_Pattern', str.__class__.__name__))
    if regexp.__class__.__name__ == 'SRE_Pattern':
        if regexp.search(text):
            return True
        else:
            return False
    if regexp.__class__.__name__ == str.__class__.__name__:
        if re.search(regexp, text, flags):
            return True
        else:
            return False

def ds_print(ds, message, io_lock=None):
    """
    Thread safe printing with DS in start line.

    :param ds:
    :param message:
    :param io_lock: object threading.Lock or threading.RLock
    """
    assert(io_lock and
           io_lock.__class__.__name__ not in (threading.Lock().__class__.__name__,
                                              threading.RLock().__class__.__name__))
    if io_lock: io_lock.acquire()
    print "{ds} : {message}".format(ds=ds, message=message)
    if io_lock: io_lock.release()

if __name__ == "__main__":
    print RE.DS_NAME.findall(open('20161205_121503_Figaro.log').read())
    print RE.DS_TYPE.findall(open('20161205_121503_Figaro.log').read())
    print RE.PRIMARY_BOF_IMAGE.findall(open('20161205_121503_Figaro.log').read())
    print RE.SECONDARY_BOF_IMAGE.findall(open('20161205_121503_Figaro.log').read())
    print RE.DIR_FILE_PREAMBLE.findall(open('20161205_121503_Figaro.log').read())
    print RE.FREE_SPACE_SIZE.findall(open('20161205_121503_Figaro.log').read())
    print RE.SW_VERSION.findall(open('20161205_121503_Figaro.log').read())
