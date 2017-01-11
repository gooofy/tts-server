# TTS-Server

Simple REST-style HTTP TTS server using

* MaryTTS, espeak and sequitur for g2p,
* MaryTTS and espeak for synthesis and
* pulseaudio for actual audio output.

Getting Started
===============

Just run

    ./tts-server -h

to get help. The TTS server by default listens on localhost port 8300 if you specify no arguments.

Protocol / API
==============

G2P (grapheme to phoneme) Conversion
------------------------------------

* GET `tts/g2p`
* args: 
  * `l`   : 'en\_US', 'de\_DE', 'fr\_FR', ...
  * `v`   : voice to use (see below for examples)
  * `e`   : 'mary', 'espeak' or 'sequitur'
  * `t`   : text or ipa to synthesize, utf-8 encoded

Returns: 

* 400 if request is invalid
* 200 OK {"ipa": "'ha\u028apt-ba\u02d0n-ho\u02d0f"}

Example:

    curl -i 'http://localhost:8300/tts/g2p?l=de&v=de&e=sequitur&t=hauptbahnhof'


Synthesize Text/IPA to WAVE
---------------------------

* GET `tts/synth`
* args: 
  * `l` : 'en\_US', 'de\_DE', 'fr\_FR', ...
  * `v` : voice to use (see below for examples)
  * `e` : 'mary' or 'espeak'
  * `m` : 'txt' or 'ipa' 
  * `t` : text or ipa to synthesize, utf-8 encoded

Returns: 

* 400 if request is invalid
* 200 OK, wave data

Example:

    curl 'http://localhost:8300/tts/synth?l=de_DE&v=bits3&e=mary&m=txt&t=hauptbahnhof' >foo.wav


Play WAV File Through PulseAudio
--------------------------------

* POST `tts/play`
* args: 
  * `async` : t to return immediately, otherwise: wait for playback to finish 

Returns: 

* 400 if request is invalid
* 200 OK otherwise

Example:

    curl -H "Content-Type: audio/wav" -X POST --data-binary @foo.wav 'http://localhost:8300/tts/play?async=t'


Requirements
============

*Note*: very incomplete.

* Python 2.7 
* Mary TTS
* espeak
* sequitur g2p

Voices
======

Which voices are available in MaryTTS depends on your installation. Here are some typical examples:

* english, male
  * `dfki-spike`
  * `dfki-obadiah`
  * `dfki-obadiah-hsmm`
  * `cmu-bdl-hsmm`
  * `cmu-rms-hsmm`
    
* english, female
  * `dfki-poppy`
  * `dfki-poppy-hsmm`
  * `dfki-prudence`
  * `dfki-prudence-hsmm`
  * `cmu-slt-hsmm`

* german, male
  * `dfki-pavoque-neutral`
  * `dfki-pavoque-neutral-hsmm`
  * `dfki-pavoque-styles`
  * `bits3`
  * `bits3-hsmm`

* german, female
  * `bits1-hsmm`

* french, male
  * `upmc-pierre-hsmm`
  * `upmc-pierre`
  * `enst-dennys-hsmm`

* french, female
  * `enst-camille`
  * `enst-camille-hsmm`
  * `upmc-jessica`
  * `upmc-jessica-hsmm`

License
=======

My own scripts as well as the data I create (i.e. lexicon and transcripts) is
LGPLv3 licensed unless otherwise noted in the script's copyright headers.

Some scripts and files are based on works of others, in those cases it is my
intention to keep the original license intact. Please make sure to check the
copyright headers inside for more information.

Author
======

Guenter Bartsch <guenter@zamia.org>

