from decimal import Decimal

from mm_std import print_json

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(params: BaseAccountParams, inst_id: str, sz: Decimal) -> None:
    client = AccountClient(params.account)
    res = await client.buy_market(inst_id, sz)
    print_debug_or_error(res, params.debug)

    print_json(res)
