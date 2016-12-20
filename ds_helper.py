import re


class RE:
    FLAGS = re.IGNORECASE
    FILE_DATE_STRING = r'\b\d\d\/\d\d\/\d\d\d\d\b'
    FILE_TIME_STRING = r'\b\d\d:\d\d[am]\b'
    PRIMARY_BOF_IMAGE = re.compile(r'primary-image\s+?(\S+)\b', FLAGS)
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
    DS_NAME = re.compile(r'ds\d-[0-9a-z]+\b', FLAGS)

    def extract(regExp, text):
        try:
            return re.findall(regExp, text, re.IGNORECASE)[0]
        except IndexError as error:
            return None

    def is_contains(regExp, text, flags = re.IGNORECASE):
        if re.search(regExp, text, flags):
            return True
        else:
            return False
