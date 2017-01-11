#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# some simple TTS server unit tests
#
# assumes server is running on localhost:8300 (the default)
#

import unittest
import json
import requests
import logging
import urllib

MARY_VOICES = {
               'en_US' : ["cmu-rms-hsmm",
                            # "dfki-spike",
                            # "dfki-obadiah",
                            # "dfki-obadiah-hsmm",
                            # "cmu-bdl-hsmm",
                            # "dfki-poppy",
                            # "dfki-poppy-hsmm",
                            # "dfki-prudence",
                            # "dfki-prudence-hsmm",
                            # "cmu-slt-hsmm"
                         ],
               
               'de_DE': ["dfki-pavoque-neutral-hsmm",
                            # "dfki-pavoque-neutral",
                            # "dfki-pavoque-styles",
                            "bits3",
                            # "bits3-hsmm",
                            # "bits1-hsmm"
                        ],
               
               'fr_FR': ["upmc-pierre-hsmm",
                            # "upmc-pierre",
                            # "upmc-jessica",
                            # "upmc-jessica-hsmm",
                            # "enst-camille",
                            # "enst-camille-hsmm",
                            # "enst-dennys-hsmm"
                        ]
              }
ESPEAK_VOICES = [ 'en', 'de', 'fr' ]

UTTS_TXT = {'en': u"Hello World", 'de': u"Hallo Welt",          'fr': u"Bonjour monde"     }
UTTS_IPA = {'en': u"hɛ-lu",       'de': u"bə-ˈtʁiːps-zʏs-teːm", 'fr': u"'bo-\u0292u\u0281" }

TTS_HOST = 'localhost'
TTS_PORT = 8300

G2P_TESTS = [
                ('en_US', 'cmu-rms-hsmm',     'mary',   'freedom',        u"'fri-d\u0259m"),
                ('de_DE', 'bits3',            'mary',   'betriebssystem', u"b\u0259-'t\u0281i\u02d0ps-z\u028fs-te\u02d0m"),
                ('fr_FR', 'upmc-pierre-hsmm', 'mary',   'bonjour',        u"'bo-\u0292u\u0281"),
                ('en',    'en',               'espeak', 'freedom',        u"f'i\u02d0d\u0259m"),
                ('de',    'de',               'espeak', 'betriebssystem', u"b\u0259t\u0281'i\u02d0psz\u028fste\u02d0m"),
            ]

class TestVoices(unittest.TestCase):

    def test_espeak(self):

        for voice in ESPEAK_VOICES:

            txt = UTTS_TXT[voice]

            args = {'l': voice,
                    'v': voice,
                    'e': 'espeak',
                    'm': 'txt',
                    't': txt.encode('utf8')}
            url = 'http://%s:%s/tts/synth?%s' % (TTS_HOST, TTS_PORT, urllib.urlencode(args))

            response = requests.get(url)

            self.assertEqual( response.status_code, 200)

    def test_mary(self):

        for locale in MARY_VOICES:
            for voice in MARY_VOICES[locale]:

                txt = UTTS_TXT[locale[:2]]

                args = {'l': locale,
                        'v': voice,
                        'e': 'mary',
                        'm': 'txt',
                        't': txt.encode('utf8')}
                url = 'http://%s:%s/tts/synth?%s' % (TTS_HOST, TTS_PORT, urllib.urlencode(args))
                                  
                logging.debug("testing voice %s %s" % (voice, url))

                response = requests.get(url)

                self.assertEqual( response.status_code, 200)

                ipa = UTTS_IPA[locale[:2]]

                args = {'l': locale,
                        'v': voice,
                        'e': 'mary',
                        'm': 'ipa',
                        't': ipa.encode('utf8')}

                url = 'http://%s:%s/tts/synth?%s' % (TTS_HOST, TTS_PORT, urllib.urlencode(args))

                logging.debug("testing voice %s IPA %s" % (voice, url))

                response = requests.get(url)

                self.assertEqual( response.status_code, 200)

    def test_g2p(self):

        for locale, voice, engine, word, ipa in G2P_TESTS:

            args = {'l': locale,
                    'v': voice,
                    'e': engine,
                    'm': 'txt',
                    't': word.encode('utf8')}
            url = 'http://%s:%s/tts/g2p?%s' % (TTS_HOST, TTS_PORT, urllib.urlencode(args))

            logging.debug("testing g2ps %s %s" % (word, url))

            response = requests.get(url)

            logging.debug("testing g2ps %s %s -> %d" % (word, url, response.status_code))

            self.assertEqual (response.status_code, 200)
            res = response.json()
            self.assertEqual (res['ipa'], ipa)

    def test_play(self):

        with open('foo.wav', 'rb') as wavf:
        
            wav = wavf.read()

            url = 'http://%s:%s/tts/play?async=t' % (TTS_HOST, TTS_PORT)
                              
            response = requests.post(url, data=wav)

            self.assertEqual (response.status_code, 200)


if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    unittest.main()

