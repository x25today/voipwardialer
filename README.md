# voipwardialer

A Voip Wardialer for the phreaking of 2020

To try VoIP Wardialer at this stage of development check it out [INSTALL.md](https://github.com/x25today/voipwardialer/blob/master/INSTALL.md)

It's actually usable as a command line tool:

```bash

$ python dialer.py call
  Usage: dialer.py call [OPTIONS] SIP_URI SIP_REG_URI SIP_USERNAME SIP_PASSWORD
                        PHONE_NUMBER MODEM_VERSION MODEM_PARITY


$ python3 dialer.py call sip:username@sip.example.com sip:sip.example.com username password +1555123456 V22 8n1
```

_LIMITATIONS_: It needs tuning and fixing on the channel quality for proper DSP Modem operations (probably echo cancellation and noise suppression) as modem carriers does not always CONNECT

# Project Goals

This project aims to provide a modern voip wardialing free software.

It's meant for seasoned and young hackers willing to play with the old good telephony system from the comfort of their notebook.

It try to overcome the telecommunication related carrier over compressed audio codec used in VoIP, by trying to negotiate carriers with speed of 300bit/s 600bit/s 1200/bit.

The software is meant also to be as simple and easy software voip dialer with modem detection, modem modulation/demodulation that finally let you interact with the remote system trough terminal emulation.

Most of the project that went working on something like this gave up due to the many complexity across telecommunication and not ready software modem stack that can be easily used and integrated.

VoIP Wardialer need to first solve this nifty problem, reaching a working sofware modem (DSP) that you can use and provide you an I/O with a remote system terminal from within your application.

# Architecture

VoIP Wardialer made up of two component:

- The VoIP Wardialer
- The Modem Server

The VoIP Wardialer is a Python 3 application that use [PJSUA](https://www.pjsip.org/pjsua.htm) VoIP Stack with [Python 3 binding](https://github.com/mgwilliams/python3-pjsip).

It does call the target phone number, detect if there's a modem answering, negotiate modem carrier with a Remote Modem Server, provide then I/O of the remote system terminal dumping it's content into a file or to standard output.

To connect the audio flow coming from the called phone number to the Modem DSP running on Modem Server:

1. VoIP Wardialer starts another SIP VoIP call to a pre-configured Asterisk (running in localhost)
2. VoIP Wardialer setup a conference bridge between the two calls (One to remote system, one to local Asterisk)
3. Asterisk-Softmodem is used by Asterisk in the Modem Server negotiate the modem carrier
4. Asterisk-Softmodem provide the I/O of the remote system termina connecting via TCP a VoIP Wardialer listener

It's a neat workflow of data going around that may require a schema.

# Roadmap

The software is not yet fully working and does require further work to achieve it's goal.

- Experiment to make DSP properly working

  - Make DSP Modem (Asterisk-Softmodem hooked to Asterisk) working properly and consistenly
  - Evaluate other Asterisk BTX Modem in place of Asterisk-Modem
  - Integrate a C native code software modem trough ctypes (Linmodem? Fisher-Modem?)

- Develop TCP Listener built-in in VoIP Wardiaer (to receive terminal I/O of remote system from Asterisk-SoftModem running in Modem Server)
- Scanning functionalities

  - Range generation
  - Session resumption
  - Logging of carrier and output of those carriers

- Multi channel parallel dialing

- Modem Detection trough Audio Sample Frequency Analysis (Use ready made [WarVox Classifiers](https://github.com/rapid7/warvox/blob/master/config/classifiers/01.default.rb))

- Modem Server Improvement

  - Modem Server Configuration Generation
  - Remote Modem Server (to run it on another machine)

- Provide interactive terminal emulation connector (ptsy/tty for use with Minicom)

- Provide a working AT hayes modem emulator to be able to be used as a VoIP software modem by existing wardialing software

# Resources

Technical resources useful for the project research

## Software Modem

Most of the complexity in this project is overcoming the problem of having any to integrate and use software modem DSP

Below several software modem resources

- [Asterisk-Softmodem](https://github.com/irrelevantdotcom/asterisk-Softmodem) fork that we use, with parity bit improvements
- [Asterisk-Softmodem](https://github.com/proquar/asterisk-Softmodem) Original Asterisk Softmodem
- [Asterisk Btx Modem](https://github.com/Casandro/btx_modem) Another Asterisk softmodem with v.23 carrier (No good: "it
  only does V.23 without negotiation")
- [Fisher Modem](https://github.com/randyrossi/fisher-modem) a potentially very cool software modem (that nobody used)
- [Linux Softmodem](https://bellard.org/linmodem/) Original Linmodem source code for integraton with linux softmodem
- [Liquid-DSP](https://github.com/jgaeddert/liquid-dsp/issues/119) improvement ideals
- [Osmocom Linmodem](http://osmocom.org/projects/linmodem/issues) cool project to hook AT hayes / RTP Procesing / PTY Terminal to Linmodem
- [IAXModem](https://sourceforge.net/p/iaxmodem/mailman/message/26647790/) and idea to use it for modem carrier (not only fax)

A nice writeup by Asterisk-Softmodem fork author [Modem Emulation - an RC2018/09 prologue](https://blog.irrelevant.com/2018/09/modem-emulation-rc201809-prologue.html)

## Supported Carriers

We plan to support only basic low bitrate carriers such as

- V21 - 300/300 baud
- V23 - 1200/75 baud
- Bell103 - 300/300 baud
- V22 - 1200/1200 baud
- V22bis - 2400/2400 baud

We do support those parity configurations:

- 8N1
- 7E1

## Other Wardialing Software

- [iWar](https://github.com/beave/iwar) Linux Terminal Analog Modem Wardialer
- [ToneLoc](https://github.com/steeve/ToneLoc) MS-DOS Analog Modem Wardialer
- [WarVox](https://github.com/rapid7/warvox) Linux IAX VoIP Wardialer with freq Detection but not Modem DSP (no Terminal)
- [Raptor's ward.c](https://0xdeadbeef.info/code/ward.c) Simple single file analog wardialer for Unix
- [WarVox 1.0 Presentation](https://dl.packetstormsecurity.net/papers/general/warvox-1.0.0.pdf)
- [2017 Defcon Talk AAPL – Automated Analog Telephone Logging](https://www.defcon.org/images/defcon-17/dc-17-presentations/defcon-17-da_beave-jfalcon-aapl-telephone_logging.pdf) on iWar/WarVox status and evolution
- [2009 Defcon Talk Metasploit Framework Telephony](https://www.blackhat.com/presentations/bh-usa-09/TRAMMELL/BHUSA09-TrammellDruid-MetasploitTele-PAPER.pdf) as an Analog Wardialer for use with Metasploit
- [THC Scan NG](https://github.com/vanhauser-thc/THC-Archive/blob/master/Tools/tsng-1.1.tar.gz) old school Linux modem wardialer with many high performance features
- [Python Advanced Wardialer](https://www.darknet.org.uk/2008/07/pawpaws-python-advanced-wardialing-system/) for ISDN scanning

# Example Modem to call around the world for testing

Below a list of modem for testing the DSP connections

- IT Dialup Number of Infinito +39771751751 (** Ascend TNT Terminal Server **)
- UK O2 CSD Data Number (PPP) +447712927927
- NL KPN (TUN\TAP) +31653141414
- DE Blup BBS +4920938143 https://www.blup-bbs.de/mailbox
- BE TAP SMSC for Proximus +32475161621 (8N1) . (It could be used to send SMS with Linux's [smsclient](http://howto.gumph.org/content/send-sms-messages-from-linux/))
- US ATT Nationwide Pager +18007247784 (2400/7E1) from [TAP Dialup Numbers](http://www.pager-enterprise.com/TAP_dialup_numbers.pdf)
- NZ New Zealand Telecom Paging +64264001283 (7E1) from [TAP Numbers](https://www.seqent.com/wp-content/uploads/2014/12/TAP_numbers-1.pdf)
- BBS with Dialup, mostly in US (up to date) https://www.telnetbbsguide.com/bbs/connection/dial-up/list/detail/
