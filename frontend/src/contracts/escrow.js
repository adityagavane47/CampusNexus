export const APPROVAL_PROGRAM = `#pragma version 11
#pragma typetrack false

main:
    intcblock 0 1 8
    bytecblock "status" "released_amount" "total_amount" "client" "freelancer" 0x151f7c75
    txn ApplicationID
    bnz main_after_if_else@2
    bytec_2
    intc_0
    app_global_put
    bytec_1
    intc_0
    app_global_put
    bytec_0
    intc_0
    app_global_put

main_after_if_else@2:
    txn NumAppArgs
    bz main___algopy_default_create@14
    txn OnCompletion
    !
    assert
    txn ApplicationID
    assert
    pushbytess 0xab65044f 0x5e09507d 0xbc929611 0xb54e51d7 0xcee44c20
    txna ApplicationArgs 0
    match create_escrow fund_escrow release_payment cancel_escrow get_info
    err

main___algopy_default_create@14:
    txn OnCompletion
    !
    txn ApplicationID
    !
    &&
    return

create_escrow:
    txna ApplicationArgs 1
    dup
    len
    pushint 32
    ==
    assert
    txna ApplicationArgs 2
    dup
    len
    intc_2
    ==
    assert
    btoi
    intc_0
    bytec_0
    app_global_get_ex
    assert
    !
    assert
    bytec_3
    txn Sender
    app_global_put
    bytec 4
    uncover 2
    app_global_put
    bytec_2
    swap
    app_global_put
    bytec_1
    intc_0
    app_global_put
    bytec_0
    intc_1
    app_global_put
    pushbytes 0x151f7c75001b457363726f772063726561746564207375636365737366756c6c79
    log
    intc_1
    return

fund_escrow:
    txn Sender
    intc_0
    bytec_3
    app_global_get_ex
    assert
    ==
    assert
    intc_0
    bytec_0
    app_global_get_ex
    assert
    intc_1
    ==
    assert
    pushbytes 0x151f7c75000d457363726f772066756e646564
    log
    intc_1
    return

release_payment:
    txna ApplicationArgs 1
    dup
    len
    intc_2
    ==
    assert
    btoi
    txn Sender
    intc_0
    bytec_3
    app_global_get_ex
    assert
    ==
    assert
    intc_0
    bytec_0
    app_global_get_ex
    assert
    intc_1
    ==
    assert
    intc_0
    bytec_1
    app_global_get_ex
    assert
    dig 1
    +
    intc_0
    bytec_2
    app_global_get_ex
    assert
    dig 1
    >=
    assert
    itxn_begin
    intc_0
    bytec 4
    app_global_get_ex
    assert
    uncover 2
    itxn_field Amount
    itxn_field Receiver
    intc_1
    itxn_field TypeEnum
    intc_0
    itxn_field Fee
    itxn_submit
    bytec_1
    dig 1
    app_global_put
    intc_0
    bytec_2
    app_global_get_ex
    assert
    >=
    bz release_payment_after_if_else@4
    bytec_0
    pushint 2
    app_global_put
    pushbytes "Escrow completed - all funds released"

release_payment_after_inlined_smart_contracts.escrow.contract.MilestoneEscrow.release_payment@5:
    dup
    len
    itob
    extract 6 2
    swap
    concat
    bytec 5
    swap
    concat
    log
    intc_1
    return

release_payment_after_if_else@4:
    pushbytes "Payment released"
    b release_payment_after_inlined_smart_contracts.escrow.contract.MilestoneEscrow.release_payment@5

cancel_escrow:
    txn Sender
    intc_0
    bytec_3
    app_global_get_ex
    assert
    ==
    assert
    intc_0
    bytec_0
    app_global_get_ex
    assert
    intc_1
    ==
    assert
    intc_0
    bytec_1
    app_global_get_ex
    assert
    !
    assert
    bytec_0
    pushint 3
    app_global_put
    pushbytes 0x151f7c750010457363726f772063616e63656c6c6564
    log
    intc_1
    return

get_info:
    intc_0
    bytec_3
    app_global_get_ex
    assert
    intc_0
    bytec 4
    app_global_get_ex
    assert
    intc_0
    bytec_2
    app_global_get_ex
    assert
    intc_0
    bytec_1
    app_global_get_ex
    assert
    intc_0
    bytec_0
    app_global_get_ex
    assert
    uncover 4
    uncover 4
    concat
    uncover 3
    itob
    concat
    uncover 2
    itob
    concat
    swap
    itob
    concat
    bytec 5
    swap
    concat
    log
    intc_1
    return
`;

export const CLEAR_PROGRAM = `#pragma version 11
#pragma typetrack false

main:
    pushint 1
    return
`;
