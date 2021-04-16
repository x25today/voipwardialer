### voipwardialer

##### What's inside:

- asterisk-conf : Asterisk 13.28.0 configuration files
- scripts : Netcat basic socket listener for testing
- dialer : Wardialer Python code

##### How to build it on Linux:

_Requirements (Tested with):_

- Python >= 3.6
- PJProject 2.9 (https://www.pjsip.org/download.htm)
- PJSua Python3 Bindings (https://github.com/mgwilliams/python3-pjsip)
- Asterisk 13.28 (https://downloads.asterisk.org/pub/telephony/asterisk/old-releases/asterisk-13.28.0.tar.gz)
- asterisk-Softmodem fork by irrelevantdotcom with added parity bits (https://github.com/irrelevantdotcom/asterisk-Softmodem)

_Build:_

- Create a Python 3.6 Virtual Environment (virtualenv -p python3.6 venv)
- Activate the virtual environment and install requirements.txt (pip install -r requirements.txt)
- Download and install Asterisk 13.28 sources
- Follow build instructions for the asterisk-Softmodem DSP (put app_softmodem.c in the Asterisk apps/ dir and do make apps).
  More details in the asterisk-Softmodem README.
- Build and install Asterisk
- Download and install PJSip 2.9 Sources
- Follow build instructions for the PJSua Python3 Bindings using the virtual environment instead of the global interpreter.
  More details in the PJSua Python3 Bindings README.
- Configure asterisk
  - mv /etc/asterisk/ /etc/asterisk.backup
  - cp -pr asterisk-conf /etc/asterisk
  - service asterisk restart

##### How to call a modem:

Activate the virtual environment:

```bash
$ . venv/bin/activate
```

Run the test socket listener (bounded on localhost:8290 according Asterisk' extension.conf) to receive the remote modem data.

```bash
$ bash scripts/modem_socket
```

Finally run the dialer script and check the output of the test socket listener, after moving into python/dialer directory.

```bash

$ python dialer.py call
  Usage: dialer.py call [OPTIONS] SIP_URI SIP_REG_URI SIP_USERNAME SIP_PASSWORD
                        PHONE_NUMBER MODEM_VERSION MODEM_PARITY


$ python3 dialer.py call sip:username@sip.example.com sip:sip.example.com username password +1555123456 V22 8n1
```

Available MODEM_VERSION:

- v21
- v23
- bell103
- v22
- v22bis

Available MODEM_PARITY:

- 7e1
- 8n1

Hit Ctrl+C to exit or wait the 60 seconds limit.
