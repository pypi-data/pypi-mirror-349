from mm_std import print_json

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(params: BaseAccountParams, inst_id: str | None) -> None:
    client = AccountClient(params.account)
    res = await client.get_order_history(inst_id)
    print_debug_or_error(res, params.debug)

    print_json(res)
