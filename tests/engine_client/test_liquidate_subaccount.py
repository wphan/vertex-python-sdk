from vertex_protocol.engine_client.types.execute import (
    LiquidateSubaccountParams,
    LiquidateSubaccountRequest,
    to_execute_request,
)
from vertex_protocol.utils.bytes32 import hex_to_bytes32


def test_liquidate_subaccount_params(
    senders: list[str], owners: list[str], liquidate_subaccount_params: dict
):
    sender = senders[0]
    liquidatee = senders[1]
    mode = liquidate_subaccount_params["mode"]
    healthGroup = liquidate_subaccount_params["healthGroup"]
    amount = liquidate_subaccount_params["amount"]
    params_from_dict = LiquidateSubaccountParams(
        **{
            "sender": sender,
            "liquidatee": liquidatee,
            "mode": mode,
            "healthGroup": healthGroup,
            "amount": amount,
        }
    )
    params_from_obj = LiquidateSubaccountParams(
        sender=sender,
        liquidatee=liquidatee,
        mode=mode,
        healthGroup=healthGroup,
        amount=amount,
    )
    bytes32_sender = LiquidateSubaccountParams(
        sender=hex_to_bytes32(senders[0]),
        liquidatee=hex_to_bytes32(senders[1]),
        mode=mode,
        healthGroup=healthGroup,
        amount=amount,
    )
    subaccount_params_sender = LiquidateSubaccountParams(
        sender={"subaccount_owner": owners[0], "subaccount_name": "default"},
        liquidatee={"subaccount_owner": owners[1], "subaccount_name": "default"},
        mode=mode,
        healthGroup=healthGroup,
        amount=amount,
    )

    assert (
        params_from_dict
        == params_from_obj
        == bytes32_sender
        == subaccount_params_sender
    )
    params_from_dict.signature = (
        "0x51ba8762bc5f77957a4e896dba34e17b553b872c618ffb83dba54878796f2821"
    )
    params_from_dict.nonce = 100000
    req_from_params = LiquidateSubaccountRequest(liquidate_subaccount=params_from_dict)
    assert req_from_params == to_execute_request(params_from_dict)
    assert req_from_params.dict() == {
        "liquidate_subaccount": {
            "tx": {
                "sender": sender.lower(),
                "liquidatee": liquidatee.lower(),
                "mode": mode,
                "healthGroup": healthGroup,
                "amount": str(amount),
                "nonce": str(params_from_dict.nonce),
            },
            "signature": params_from_dict.signature,
        }
    }
