# voipwardialer
A Voip Wardialer for the phreaking of 2020

# Intro
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

The VoIP Wardialer is a Python 3 application that use [PJSUA](https://www.pjsip.org/pjsua.htm) VoIP Stack with [Python 3 binding](https://github.com/mgwilliams/python3-pjsip) to call the target phone number, then detect if there's a modem carrier trough frequency, and if C that if possitive try to establish a modem carier

Given tThe MVP is meant to be ready for experiment and contribute in the making of VoIP Wardialer software


# Try it out
The MVP is meant to be ready for experiment and contribute in the making of VoIP Wardialer software

To use VoIP Wardialer you need at least:
* A Linux Debian machine
* A SIP account at VoIP Provider or your own SIP Server
* A phone number to call where modem answer

To install it we first need to build the PJSUA VoIP stack, that will then be used as telephony engine:
TODO: Describe how to install PJSUA


TODO: How to we deliver Asterisk? By a docker image or by apt-get install asterisk + copy configuration files in /etc/asterisk?

Tech specs are:
* Python 3
* PJSUA library for SIP/VoIP dialing and Conference Bridging
* Remote Modem DSP Server (An Asterisk with asterisk-softmodem)



# Roadmap
* Experiment to make DSP properly working
  * Make DSP Modem (hooked to Asterisk) working properly and consistenly (this is the most important hit of the project!)
  * Integrate a C native code software modem
* Modem Detection trough Audio Sample Frequency Analysis (like [WarVox Classifiers](https://github.com/rapid7/warvox/blob/master/config/classifiers/01.default.rb)
* Modem Server Configuration Generation (If that's the path for the DSP)
* Scanning functionalities 
  * Range generation
  * Session resumption
  * Logging of carrier and output of those carriers
* Multi channel parallel dialing
* Provide interactive terminal emulation connector (ptsy/tty for use with Minicom or other terminal emulation sw/lib)


# Resources
Making a project like this implies a lot of complexity

## Software Modem
Most of them with some specific limit or integration complexity
* [Fisher Modem](https://github.com/randyrossi/fisher-modem)

# Example Modem to call around the world for testing
TODO: List 10-15 modem to call that works across various countries
