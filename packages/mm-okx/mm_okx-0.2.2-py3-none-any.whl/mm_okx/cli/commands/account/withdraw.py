from decimal import Decimal

from mm_std import print_json

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(*, params: BaseAccountParams, ccy: str, amt: Decimal, fee: Decimal, to_addr: str, chain: str | None) -> None:
    client = AccountClient(params.account)
    res = await client.withdraw(ccy=ccy, amt=amt, fee=fee, to_addr=to_addr, chain=chain)
    print_debug_or_error(res, params.debug)

    print_json(res)
