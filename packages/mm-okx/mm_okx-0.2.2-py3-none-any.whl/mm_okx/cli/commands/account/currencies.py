from mm_std import print_table

from mm_okx.cli.commands.account_commands import BaseAccountParams
from mm_okx.cli.utils import print_debug_or_error
from mm_okx.clients.account import AccountClient


async def run(params: BaseAccountParams, ccy: str | None) -> None:
    client = AccountClient(params.account)
    res = await client.get_currencies(ccy)
    print_debug_or_error(res, params.debug)

    headers = ["ccy", "chain", "can_dep", "can_wd", "max_fee", "min_fee", "max_wd", "min_wd"]
    rows = [
        [
            currency.ccy,
            currency.chain,
            currency.can_dep,
            currency.can_wd,
            currency.max_fee,
            currency.min_fee,
            currency.max_wd,
            currency.min_wd,
        ]
        for currency in res.unwrap()
    ]
    print_table("Currencies", headers, rows)
