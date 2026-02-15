/**
 * CampusNexus - Compiled Escrow Contract Artifacts
 * Generated from smart_contracts/escrow/contract.py
 */

// Approval Program (TEAL v11)
export const APPROVAL_PROGRAM = `#pragma version 11
#pragma typetrack false

// algopy.arc4.ARC4Contract.approval_program() -> uint64:
main:
    intcblock 0 1 8
    bytecblock "status" "released_amount" "total_amount" "client" "freelancer" 0x151f7c75
    txn ApplicationID
    bnz main_after_if_else@2
    // smart_contracts/escrow/contract.py:23
    // self.total_amount = GlobalState(UInt64(0))
    bytec_2 // "total_amount"
    intc_0 // 0
    app_global_put
    // smart_contracts/escrow/contract.py:24
    // self.released_amount = GlobalState(UInt64(0))
    bytec_1 // "released_amount"
    intc_0 // 0
    app_global_put
    // smart_contracts/escrow/contract.py:25
    // self.status = GlobalState(UInt64(0))  # 0=inactive, 1=active, 2=completed, 3=cancelled
    bytec_0 // "status"
    intc_0 // 0
    app_global_put

main_after_if_else@2:
    // smart_contracts/escrow/contract.py:9
    // class MilestoneEscrow(ARC4Contract):
    txn NumAppArgs
    bz main___algopy_default_create@14
    txn OnCompletion
    !
    assert
    txn ApplicationID
    assert
    pushbytess 0xab65044f 0x5e09507d 0xbc929611 0xb54e51d7 0xcee44c20 // method "create_escrow(address,uint64)string", method "fund_escrow()string", method "release_payment(uint64)string", method "cancel_escrow()string", method "get_info()(address,address,uint64,uint64,uint64)"
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


// smart_contracts.escrow.contract.MilestoneEscrow.create_escrow[routing]() -> void:
create_escrow:
    // smart_contracts/escrow/contract.py:27
    // @abimethod()
    txna ApplicationArgs 1
    dup
    len
    pushint 32
    ==
    assert // invalid number of bytes for arc4.static_array<arc4.uint8, 32>
    txna ApplicationArgs 2
    dup
    len
    intc_2 // 8
    ==
    assert // invalid number of bytes for arc4.uint64
    btoi
    // smart_contracts/escrow/contract.py:30
    // assert self.status.value == UInt64(0), "Escrow already exists"
    intc_0 // 0
    bytec_0 // "status"
    app_global_get_ex
    assert // check self.status exists
    !
    assert // Escrow already exists
    // smart_contracts/escrow/contract.py:32
    // self.client.value = Txn.sender
    bytec_3 // "client"
    txn Sender
    app_global_put
    // smart_contracts/escrow/contract.py:33
    // self.freelancer.value = freelancer_addr
    bytec 4 // "freelancer"
    uncover 2
    app_global_put
    // smart_contracts/escrow/contract.py:34
    // self.total_amount.value = amount
    bytec_2 // "total_amount"
    swap
    app_global_put
    // smart_contracts/escrow/contract.py:35
    // self.released_amount.value = UInt64(0)
    bytec_1 // "released_amount"
    intc_0 // 0
    app_global_put
    // smart_contracts/escrow/contract.py:36
    // self.status.value = UInt64(1)
    bytec_0 // "status"
    intc_1 // 1
    app_global_put
    // smart_contracts/escrow/contract.py:27
    // @abimethod()
    pushbytes 0x151f7c75001b457363726f772063726561746564207375636365737366756c6c79
    log
    intc_1 // 1
    return


// smart_contracts.escrow.contract.MilestoneEscrow.fund_escrow[routing]() -> void:
fund_escrow:
    // smart_contracts/escrow/contract.py:43
    // assert Txn.sender == self.client.value, "Only client can fund"
    txn Sender
    intc_0 // 0
    bytec_3 // "client"
    app_global_get_ex
    assert // check self.client exists
    ==
    assert // Only client can fund
    // smart_contracts/escrow/contract.py:44
    // assert self.status.value == UInt64(1), "Escrow not active"
    intc_0 // 0
    bytec_0 // "status"
    app_global_get_ex
    assert // check self.status exists
    intc_1 // 1
    ==
    assert // Escrow not active
    // smart_contracts/escrow/contract.py:40
    // @abimethod()
    pushbytes 0x151f7c75000d457363726f772066756e646564
    log
    intc_1 // 1
    return


// smart_contracts.escrow.contract.MilestoneEscrow.release_payment[routing]() -> void:
release_payment:
    // smart_contracts/escrow/contract.py:48
    // @abimethod()
    txna ApplicationArgs 1
    dup
    len
    intc_2 // 8
    ==
    assert // invalid number of bytes for arc4.uint64
    btoi
    // smart_contracts/escrow/contract.py:51
    // assert Txn.sender == self.client.value, "Only client can release"
    txn Sender
    intc_0 // 0
    bytec_3 // "client"
    app_global_get_ex
    assert // check self.client exists
    ==
    assert // Only client can release
    // smart_contracts/escrow/contract.py:52
    // assert self.status.value == UInt64(1), "Escrow not active"
    intc_0 // 0
    bytec_0 // "status"
    app_global_get_ex
    assert // check self.status exists
    intc_1 // 1
    ==
    assert // Escrow not active
    // smart_contracts/escrow/contract.py:53
    // assert self.released_amount.value + amount <= self.total_amount.value, "Amount exceeds total"
    intc_0 // 0
    bytec_1 // "released_amount"
    app_global_get_ex
    assert // check self.released_amount exists
    dig 1
    +
    intc_0 // 0
    bytec_2 // "total_amount"
    app_global_get_ex
    assert // check self.total_amount exists
    dig 1
    >=
    assert // Amount exceeds total
    // smart_contracts/escrow/contract.py:55-59
    // # Transfer to freelancer
    // itxn.Payment(
    //     receiver=self.freelancer.value,
    //     amount=amount,
    // ).submit()
    itxn_begin
    // smart_contracts/escrow/contract.py:57
    // receiver=self.freelancer.value,
    intc_0 // 0
    bytec 4 // "freelancer"
    app_global_get_ex
    assert // check self.freelancer exists
    uncover 2
    itxn_field Amount
    itxn_field Receiver
    // smart_contracts/escrow/contract.py:55-56
    // # Transfer to freelancer
    // itxn.Payment(
    //     receiver=self.freelancer.value,
    //     amount=amount,
    // ).submit()
    intc_1 // pay
    itxn_field TypeEnum
    intc_0 // 0
    itxn_field Fee
    // smart_contracts/escrow/contract.py:55-59
    // # Transfer to freelancer
    // itxn.Payment(
    //     receiver=self.freelancer.value,
    //     amount=amount,
    // ).submit()
    itxn_submit
    // smart_contracts/escrow/contract.py:61
    // self.released_amount.value = self.released_amount.value + amount
    bytec_1 // "released_amount"
    dig 1
    app_global_put
    // smart_contracts/escrow/contract.py:63-64
    // # Check if fully released
    // if self.released_amount.value >= self.total_amount.value:
    intc_0 // 0
    bytec_2 // "total_amount"
    app_global_get_ex
    assert // check self.total_amount exists
    >=
    bz release_payment_after_if_else@4
    // smart_contracts/escrow/contract.py:65
    // self.status.value = UInt64(2)  # completed
    bytec_0 // "status"
    pushint 2
    app_global_put
    // smart_contracts/escrow/contract.py:66
    // return String("Escrow completed - all funds released")
    pushbytes "Escrow completed - all funds released"

release_payment_after_inlined_smart_contracts.escrow.contract.MilestoneEscrow.release_payment@5:
    // smart_contracts/escrow/contract.py:48
    // @abimethod()
    dup
    len
    itob
    extract 6 2
    swap
    concat
    bytec 5 // 0x151f7c75
    swap
    concat
    log
    intc_1 // 1
    return

release_payment_after_if_else@4:
    // smart_contracts/escrow/contract.py:68
    // return String("Payment released")
    pushbytes "Payment released"
    // smart_contracts/escrow/contract.py:48
    // @abimethod()
    b release_payment_after_inlined_smart_contracts.escrow.contract.MilestoneEscrow.release_payment@5


// smart_contracts.escrow.contract.MilestoneEscrow.cancel_escrow[routing]() -> void:
cancel_escrow:
    // smart_contracts/escrow/contract.py:73
    // assert Txn.sender == self.client.value, "Only client can cancel"
    txn Sender
    intc_0 // 0
    bytec_3 // "client"
    app_global_get_ex
    assert // check self.client exists
    ==
    assert // Only client can cancel
    // smart_contracts/escrow/contract.py:74
    // assert self.status.value == UInt64(1), "Escrow not active"
    intc_0 // 0
    bytec_0 // "status"
    app_global_get_ex
    assert // check self.status exists
    intc_1 // 1
    ==
    assert // Escrow not active
    // smart_contracts/escrow/contract.py:75
    // assert self.released_amount.value == UInt64(0), "Cannot cancel after release"
    intc_0 // 0
    bytec_1 // "released_amount"
    app_global_get_ex
    assert // check self.released_amount exists
    !
    assert // Cannot cancel after release
    // smart_contracts/escrow/contract.py:77
    // self.status.value = UInt64(3)  # cancelled
    bytec_0 // "status"
    pushint 3
    app_global_put
    // smart_contracts/escrow/contract.py:70
    // @abimethod()
    pushbytes 0x151f7c750010457363726f772063616e63656c6c6564
    log
    intc_1 // 1
    return


// smart_contracts.escrow.contract.MilestoneEscrow.get_info[routing]() -> void:
get_info:
    // smart_contracts/escrow/contract.py:84
    // self.client.value,
    intc_0 // 0
    bytec_3 // "client"
    app_global_get_ex
    assert // check self.client exists
    // smart_contracts/escrow/contract.py:85
    // self.freelancer.value,
    intc_0 // 0
    bytec 4 // "freelancer"
    app_global_get_ex
    assert // check self.freelancer exists
    // smart_contracts/escrow/contract.py:86
    // self.total_amount.value,
    intc_0 // 0
    bytec_2 // "total_amount"
    app_global_get_ex
    assert // check self.total_amount exists
    // smart_contracts/escrow/contract.py:87
    // self.released_amount.value,
    intc_0 // 0
    bytec_1 // "released_amount"
    app_global_get_ex
    assert // check self.released_amount exists
    // smart_contracts/escrow/contract.py:88
    // self.status.value,
    intc_0 // 0
    bytec_0 // "status"
    app_global_get_ex
    assert // check self.status exists
    // smart_contracts/escrow/contract.py:80
    // @abimethod(readonly=True)
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
    bytec 5 // 0x151f7c75
    swap
    concat
    log
    intc_1 // 1
    return
`;

// Clear Program (TEAL v11)
export const CLEAR_PROGRAM = `#pragma version 11
#pragma typetrack false

// algopy.arc4.ARC4Contract.clear_state_program() -> uint64:
main:
    pushint 1
    return
`;
