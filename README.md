# voipwardialer
A Voip Wardialer for the phreaking of 2020

# Intro
This project aims to provide a modern voip wardialing free software.

It's meant for seasoned and young hackers willing to play with the old good telephony system from the comfort of their notebook.

# Try it out

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
* Modem Server Configuration Generation (If that's the path for the DSP)
* Scanning functionalities 
  * Range generation
  * Session resumption
  * Logging of carrier and output of those carriers
* Multi channel parallel dialing
* Provide interactive terminal emulation connector (ptsy/tty for use with Minicom or other terminal emulation sw/lib)


# Resources
Making a project

## Software Modem
Most of them with some specific limit or integration complexity
* [https://github.com/randyrossi/fisher-modem Fisher Modem]

# Example Modem to call around the world for testing
TODO: List 10-15 modem to call that works across various countries
