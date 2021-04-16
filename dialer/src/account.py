from __future__ import print_function

import time

import pjsua


class Account(pjsua.CallCallback):
    def __init__(self,
                 pjsua_lib,
                 call=None,
                 on_connect=None,
                 on_disconnect=None,
                 call_id=None):
        pjsua.CallCallback.__init__(self, call)
        self.pjsua_lib = pjsua_lib
        self.on_disconnect = on_disconnect
        self.on_connect = on_connect
        self.call_id = call_id

    def on_state(self):
        print(
            "Call with",
            self.call.info().remote_uri,
        )
        print(
            "is",
            self.call.info().state_text,
        )
        print(
            "last code =",
            self.call.info().last_code,
        )
        print("(" + self.call.info().last_reason + ")")
        print("#############")

        if self.call.info().media_state == pjsua.MediaState.ACTIVE:
            print("Call Media state is ACTIVE")

        if self.call.info().state == pjsua.CallState.CONNECTING:
            print("Connecting")

        elif self.call.info().state == pjsua.CallState.CONFIRMED:
            print("Call answered")
            self.on_connect(self.call_id)

        elif self.call.info().state == pjsua.CallState.DISCONNECTED:
            current_call = None
            print("Current call is", current_call)
            self.on_disconnect(self.call_id)

        elif self.call.info().state:
            print("Not managed state: %s" % self.call.info().state)

    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pjsua.MediaState.ACTIVE:
            print("Media is now active")
        else:
            print("Media is inactive")
