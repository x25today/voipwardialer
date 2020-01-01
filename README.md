# voipwardialer
A Voip Wardialer for the phreaking of 2020

## Intro
This project aims to provide a modern voip wardialing free software.

It's meant for seasoned and young hackers willing to play with the old good telephony system from the comfort of their notebook.

It try to overcome the telecommunication related carrier over compressed audio codec used in VoIP, by trying to negotiate carriers with speed of 300bit/s 600bit/s 1200/bit. 

The software is meant also to be as simple and easy software voip dialer with modem deteciton, modem modulation/demodulation that finally let you interact with the remote system trough terminal emulation.

Most of the project that went working on something like this gave up due to the many complexity across telecommunication and not ready software modem stack that can be easily used and integrated.

VoIP Wardialer need to first solve this nifty problem, reaching a working sofware modem (DSP) that you can use and provide you an I/O with a remote system terminal from within your application.

# Archicture
VoIP Wardialer made up of two component:
- The VoIP Wardialer
- The Modem Server

The VoIP Wardialer is a Python 3 application that use [PJSUA](https://www.pjsip.org/pjsua.htm) VoIP Stack with [Python 3 binding](https://github.com/mgwilliams/python3-pjsip).

It does call the target phone number,  detect if there's a modem answering, negotiate modem carrier with a Remote Modem Server, provide then I/O of the remote system terminal dumping it's content into a file or to standard output.

To connect the audio flow coming from the called phone number to the Modem DSP running on Modem Server:

1. VoIP Wardialer starts another SIP VoIP call to a pre-configured Asterisk (running in localhost)
2. VoIP Wardialer setup a conference bridge between the two calls (One to remote system, one to local Asterisk)
3. Asterisk-Softmodem is used by Asterisk in the Modem Server negotiate the modem carrier
4. Asterisk-Softmodem provide the I/O of the remote system termina connecting via TCP a VoIP Wardialer listener

It's a neat workflow of data going around that may require a schema.

# Try it out
The MVP is meant to be ready for experiment and contribute in the making of VoIP Wardialer software

To use VoIP Wardialer you need at least:
* A Linux Debian machine
* A SIP account at VoIP Provider or your own SIP Server
* A phone number to call where modem answer

To install it we first need to build the PJSUA VoIP stack, that will then be used as telephony engine:
TODO: Describe how to install PJSUA


TODO: How to we deliver Asterisk? By a docker image or by apt-get install asterisk + copy configuration files in /etc/asterisk?

# Roadmap

The software is not yet fully working and does requrire further work to achieve it's goal. 

* Experiment to make DSP properly working
  * Make DSP Modem (hooked to Asterisk) working properly and consistenly (this is the most important hit of the project!)
  * Try Asterisk BTX Modem in place of Asterisk-Modem?
  * Integrate a C native code software modem (Linmodem? Fisher-Modem?)
  
* Scanning functionalities 
  * Range generation
  * Session resumption
  * Logging of carrier and output of those carriers
  * Modem Detection trough Audio Sample Frequency Analysis (like [WarVox Classifiers](https://github.com/rapid7/warvox/blob/master/config/classifiers/01.default.rb)
* Multi channel parallel dialing

* Modem Server Improvement
  * Modem Server Configuration Generation
  * Remote Modem Server (to run it on another machine)

* Provide interactive terminal emulation connector (ptsy/tty for use with Minicom)

# Resources
Technical resources useful for the project research 

## Software Modem
Most of the complexity in this project is overcoming the problem of having any to integrate and use software modem DSP

Below several software modem resources
* [Asterisk-Softmodem](https://github.com/irrelevantdotcom/asterisk-Softmodem) fork that we use, with parity bit improvements
* [Asterisk-Softmodem](https://github.com/proquar/asterisk-Softmodem) Original Asterisk Softmodem
* [Asterisk Btx Modem](https://github.com/Casandro/btx_modem) Another Asterisk softmodem with v.23 carrier
* [Fisher Modem](https://github.com/randyrossi/fisher-modem) a potentially very cool software modem (that nobody used)
* [Linux Softmodem](https://bellard.org/linmodem/) Original Linmodem source code for integraton with linux softmodem
* [Liquid-DSP](https://github.com/jgaeddert/liquid-dsp/issues/119) improvement ideals

A nice writeup by Asterisk-Softmodem fork author  (Modem Emulation - an RC2018/09 prologue](https://blog.irrelevant.com/2018/09/modem-emulation-rc201809-prologue.html) 


## Tech specs
* Python 3 code
* PJSUA library for SIP/VoIP dialing and Conference Bridging
* Remote Modem DSP Server (An Asterisk [Asterisk-Softmodem](https://github.com/irrelevantdotcom/asterisk-Softmodem))

## Supported Carriers
We plan to support only basic low bitrate carriers such as

* V21        - 300/300 baud 
* V23        - 1200/75 baud 
* Bell103    - 300/300 baud 
* V22        - 1200/1200 baud 
* V22bis     - 2400/2400 baud

# Example Modem to call around the world for testing
TODO: List 10-15 modem to call that works across various countries to make experiments
