from mm_std import print_table

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(params: BaseAccountParams, ccy: str) -> None:
    client = AccountClient(params.account)
    res = await client.get_deposit_address(ccy)
    print_debug_or_error(res, params.debug)

    headers = ["ccy", "chain", "address"]

    rows = [[a.ccy, a.chain, a.addr] for a in res.unwrap()]

    print_table(title="Deposit Address", columns=headers, rows=rows)
