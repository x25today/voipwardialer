import typing

import click
from src.account import Account
from src.dialer import Dialer
from src.modem import Modem


@click.group(name="dialer")
def main():
    pass


ModemData = typing.NamedTuple(
    "ModemData",
    (
        ("account_id", str),
        ("local_modem_uri", str),
        ("registration_uri", str),
        ("username", str),
        ("password", str),
    ),
)


def get_modem_data(modem_version, modem_parity, modem_server_host):
    MODEMS_INDEX = {
        "v21-7e1": 121,
        "v22-7e1": 122,
        "v23-7e1": 123,
        "bell103-7e1": 124,
        "v22bis-7e1": 125,
        "v21-8n1": 221,
        "v22-8n1": 222,
        "v23-8n1": 223,
        "bell103-8n1": 224,
        "v22bis-8n1": 225,
    }
    modem_extension = MODEMS_INDEX["{}-{}".format(modem_version.lower(),
                                                  modem_parity.lower())]
    return ModemData(
        "sip:11111",
        "sip:{}@{}".format(modem_extension, modem_server_host),
        "sip:{}".format(modem_server_host),
        "11111",
        "secret",
    )


dialer = Dialer(Account, Modem)


@main.command()
@click.argument("sip-uri")
@click.argument("sip-reg-uri")
@click.argument("sip-username")
@click.argument("sip-password")
@click.argument("phone-number")
@click.argument("modem-version")
@click.argument("modem-parity")
@click.option("--modem-server", default="localhost", help="Modem pool server")
@click.option("--logfile", default="/tmp/wardialer.log")
def call(
    sip_uri,
    sip_reg_uri,
    sip_username,
    sip_password,
    phone_number,
    modem_version,
    modem_parity,
    modem_server,
    logfile,
):
    modem_alias = "{}-{}".format(modem_version, modem_parity)
    modem_data = get_modem_data(modem_version, modem_parity, modem_server)
    dialer.add_modem(
        modem_alias,
        modem_data.account_id,
        modem_data.local_modem_uri,
        modem_data.registration_uri,
        modem_data.username,
        modem_data.password,
    ).add_account(phone_number, sip_uri, sip_reg_uri, sip_username,
                  sip_password)
    current_call = dialer.dial(phone_number, modem_alias, phone_number)


if __name__ == "__main__":
    try:
        main()
    finally:
        dialer.close()
