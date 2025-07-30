from decimal import Decimal

from mm_std import print_table

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(params: BaseAccountParams, ccy: str, amt: Decimal) -> None:
    client = AccountClient(params.account)
    res = await client.transfer_to_funding(ccy, amt)
    print_debug_or_error(res, params.debug)

    headers = ["trans_id", "ccy", "client_id", "from", "amt", "to"]
    rows = [[t.trans_id, t.ccy, t.client_id, t.from_, t.amt, t.to] for t in res.unwrap()]
    print_table("Transfer to Funding", headers, rows)
