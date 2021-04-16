import hashlib
import logging
import random
import sys
import threading
import time
import typing
from enum import Enum

import pjsua
from src import types


class EndpointType(Enum):
    ACCOUNT = 1
    MODEM = 2


class Dialer:
    def __init__(self, account_cb: pjsua.CallCallback,
                 modem_cb: pjsua.CallCallback):
        self.accounts = {}
        self.modems = {}
        self.transports = {}
        self.lib = None
        self._account_cb = account_cb
        self._modem_cb = modem_cb
        self._init_lib()
        self._calls = {}
        self._modem_calls = {}

    @staticmethod
    def _get_call_id(msisdn: str, modem: str, account: str) -> str:
        return hashlib.sha256("{}{}{}".format(msisdn, modem,
                                              account).encode()).hexdigest()

    def _msisdn_to_uri(self, msisdn: str, account: str):
        return "sip:{}@{}".format(
            msisdn,
            self.accounts[account]["meta"]["registration_uri"].replace(
                "sip:", ""),
        )

    def _get_callback(self, endpoint_type: EndpointType, call_id=None):
        return {
            EndpointType.ACCOUNT:
            lambda: self._account_cb(
                self.lib,
                on_connect=self._on_remote_connect,
                on_disconnect=self._on_remote_disconnected,
                call_id=call_id,
            ),
            EndpointType.MODEM:
            lambda: self._modem_cb(
                self.lib, call_id=call_id, on_connect=self._on_modem_connect),
        }[endpoint_type]()

    def _init_lib(self) -> None:
        self.lib = pjsua.Lib()
        self.lib.init(log_cfg=pjsua.LogConfig(level=logging.DEBUG))
        pjsua_port = random.randint(5080, 6080)
        self.transports = dict(t1=self.lib.create_transport(
            pjsua.TransportType.UDP, pjsua.TransportConfig(pjsua_port)))
        self.lib.start()
        self.lib.handle_events()

    def add_account(
        self,
        alias: str,
        account_id: str,
        registration_uri: str,
        username: str,
        password: str,
        meta: typing.Dict = None,
    ) -> "Dialer":
        print("Adding account")
        assert not self.accounts.get(alias), "Name clash"
        self.accounts[alias] = {
            "endpoint":
            self._create_endpoint(account_id, registration_uri, username,
                                  password),
            "meta":
            meta or {
                "registration_uri": registration_uri
            },
        }
        return self

    def add_modem(
        self,
        alias: str,
        account_id: str,
        local_modem_uri: str,
        registration_uri: str,
        username: str,
        password: str,
        meta: typing.Dict = None,
    ) -> "Dialer":
        print("Adding modem")
        assert not self.modems.get(alias), "Name clash"
        self.modems[alias] = {
            "endpoint":
            self._create_endpoint(account_id, registration_uri, username,
                                  password),
            "meta":
            meta or {
                "local_uri": local_modem_uri,
            },
        }
        return self

    def _create_endpoint(self, account_id: str, registration_uri: str,
                         username: str, password: str):
        class MyAccountCallback(pjsua.AccountCallback):
            sem = None

            def __init__(self, account=None):
                pjsua.AccountCallback.__init__(self, account)

            def wait(self):
                self.sem = threading.Semaphore(0)
                self.sem.acquire()

            def on_reg_state(self):
                if self.sem:
                    if self.account.info().reg_status >= 200:
                        self.sem.release()

        acc_cfg = pjsua.AccountConfig()
        acc_cfg.id = account_id
        acc_cfg.reg_uri = registration_uri
        acc_cfg.auth_cred = [pjsua.AuthCred("*", username, password)]
        acc_cb = MyAccountCallback()
        acc = self.lib.create_account(acc_cfg, cb=acc_cb)
        print("\n")
        print("Registering %s" % registration_uri)
        acc_cb.wait()
        reg_status = acc.info().reg_status
        reg_reason = acc.info().reg_reason
        if reg_status != 200:
            print("Registration failed (%s) status= %s (%s)" %
                  (registration_uri, reg_status, reg_reason))
            sys.exit(1)
        print("Registration completed (%s) status= %s (%s)" %
              (registration_uri, reg_status, reg_reason))
        return acc

    def dial(self, msisdn: str, modem: str, account: str) -> types.Call:
        print("Dialing %s with modem %s" % (msisdn, modem))
        in_call = True
        _call_id = self._get_call_id(msisdn, modem, account)
        print("Calling", msisdn)
        call = self.accounts[account]["endpoint"].make_call(
            self._msisdn_to_uri(msisdn, account),
            cb=self._get_callback(EndpointType.ACCOUNT, call_id=_call_id),
        )
        self._calls[_call_id] = types.Call(
            call_id=_call_id,
            call=call,
            msisdn=msisdn,
            modem=modem,
            account=account,
            call_endpoint=self.accounts[account]["endpoint"],
            modem_endpoint=self.modems[modem]["endpoint"],
        )
        while self._calls.get(_call_id):
            time.sleep(1)

    def _on_remote_disconnected(self, call_id, remove=True):
        print("Closing", call_id)
        call: types.Call = self._calls.get(call_id)
        if not call:
            return
        try:
            print("Hanging up call")
            call.call.hangup()
        except pjsua.Error as e:
            print(e)
        try:
            print("Hanging up modem")
            modem_call = self._modem_calls.pop(call_id, None)
            if modem_call:
                modem_call.hangup()
        except pjsua.Error as e:
            print(e)
        remove and self._calls.pop(call_id)

    def _on_remote_connect(self, call_id):
        print("Remote endpoint connected")
        modem_alias = self._calls[call_id].modem
        modem = self.modems[modem_alias]["endpoint"]
        print("Calling modem Endpoint")
        modem_call = modem.make_call(
            self.modems[modem_alias]["meta"]["local_uri"],
            cb=self._get_callback(EndpointType.MODEM, call_id=call_id),
        )
        self._modem_calls[call_id] = modem_call

    def _on_modem_connect(self, call_id):
        modem_call = self._modem_calls[call_id]
        call = self._calls[call_id]

        modem_info = modem_call.info()
        call_info = call.call.info()
        print("Bridging call & modem")
        self.lib.conf_connect(call_info.conf_slot, modem_info.conf_slot)
        self.lib.conf_connect(modem_info.conf_slot, call_info.conf_slot)

        print("Bridged call & modem")
        print(call_info.__dict__, "\n", modem_info.__dict__)
        # Uncomment this lines to activate audio
        print("Activating audio")
        self.lib.conf_connect(call_info.conf_slot, 0)
        self.lib.conf_connect(modem_info.conf_slot, 0)
        # End audio activation

    def close(self):
        for call_id in self._calls.keys():
            self._on_remote_disconnected(call_id, remove=False)
        self._unregister_endpoints()
        print("Closing")

    def _unregister_endpoints(self):
        for account in self.accounts.values():
            try:
                account["endpoint"].set_registration(False)
            except pjsua.Error as e:
                print(e)
        for modem in self.modems.values():
            try:
                modem["endpoint"].set_registration(False)
            except pjsua.Error as e:
                print(e)
