import time

import pjsua


class Modem(pjsua.CallCallback):
    def __init__(self, pjsua_lib, call=None, call_id=None, on_connect=None):
        pjsua.CallCallback.__init__(self, call)
        self.pjsua_lib = pjsua_lib
        self.on_connect = on_connect
        self.call_id = call_id

    def on_state(self):
        if self.call.info().media_state == pjsua.MediaState.ACTIVE:
            print("Modem Media state is ACTIVE")

        if self.call.info().state == pjsua.CallState.CONFIRMED:
            print("Modem Connected")
            if self.call.info().media_state == pjsua.MediaState.ACTIVE:
                # FIXME - This sleep is needed to avoid race conditions with remote DSP
                # It would be nice to find the proper way to fire on_connect callback.
                time.sleep(3)
                self.on_connect(self.call_id)
            else:
                print("Media state not ready")

    # Notification when call's media state has changed.
    def on_media_state(self):
        pass
