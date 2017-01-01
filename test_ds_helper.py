import unittest

from threading import Lock, RLock

import re

from ds_helper import RE, is_contains, extract, ds_print


class TestDsHelper(unittest.TestCase):
    def setUp(self):
        self._sample_text = r"""A:ds3-kha3# show version
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
        self._ds = 'localhost'
        self._message = 'message'
        self._Lock = Lock()
        self._RLock = RLock()
        self._fake_lock = 'lock'
        self._findall = re.findall

    def test_is_contains(self):
        self.assertTrue(is_contains(RE.DS_NAME, self._sample_text))
        self.assertTrue(is_contains(RE.FILE_SIZE_PREAMBLE, self._sample_text))
        self.assertFalse(is_contains(RE.DS_NAME, ''))
        self.assertRaises(AssertionError, is_contains, None, self._sample_text)

    def test_extract(self):
        self.assertIsNotNone(extract(RE.DS_NAME, self._sample_text))
        self.assertIsNotNone(extract(RE.FILE_SIZE_PREAMBLE, self._sample_text))
        self.assertEqual(extract(RE.DS_NAME, ''), "")
        self.assertRaises(AssertionError, extract, 0, self._sample_text)

    def test_ds_print(self):
        called = ds_print
        self.assertRaises(AssertionError, called, self._ds, self._message, self._fake_lock)
        self.assertIsNone(called(self._ds, self._message, self._Lock))
        self.assertIsNone(called(self._ds, self._message, self._RLock))
        self.assertIsNone(called(self._ds, self._message, None))

    def test_FILE_SIZE_PREAMBLE(self):
        regexp = RE.FILE_SIZE_PREAMBLE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_PRIMARY_BOF_IMAGE(self):
        regexp = RE.PRIMARY_BOF_IMAGE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_SECONDARY_BOF_IMAGE(self):
        regexp = RE.SECONDARY_BOF_IMAGE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_FILE_DATE(self):
        regexp = RE.FILE_DATE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_FILE_TIME(self):
        regexp = RE.FILE_TIME
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_DIR_FILE_PREAMBLE(self):
        regexp = RE.DIR_FILE_PREAMBLE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_DS_TYPE(self):
        regexp = RE.DS_TYPE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_SW_VERSION(self):
        regexp = RE.SW_VERSION
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_FREE_SPACE_SIZE(self):
        regexp = RE.FREE_SPACE_SIZE
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])

    def test_DS_NAME(self):
        regexp = RE.DS_NAME
        self.assertIsNotNone(self._findall(regexp, self._sample_text))
        self.assertListEqual(self._findall(regexp, ''), [])


if __name__ == '__main__':
    unittest.main()
