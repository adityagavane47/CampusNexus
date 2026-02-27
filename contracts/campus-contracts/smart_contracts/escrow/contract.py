from algopy import ARC4Contract, GlobalState, UInt64, Account, String, Txn, itxn
from algopy.arc4 import abimethod

class MilestoneEscrow(ARC4Contract):

    def __init__(self) -> None:
        self.client = GlobalState(Account)
        self.freelancer = GlobalState(Account)
        self.total_amount = GlobalState(UInt64(0))
        self.released_amount = GlobalState(UInt64(0))
        self.status = GlobalState(UInt64(0))

    @abimethod(allow_actions=["NoOp", "OptIn"])
    def create_escrow(self, freelancer_addr: Account, amount: UInt64) -> String:

        assert self.status.value == UInt64(0), "Escrow already initialized"
        
        self.client.value = Txn.sender
        self.freelancer.value = freelancer_addr
        self.total_amount.value = amount
        self.released_amount.value = UInt64(0)
        self.status.value = UInt64(1)
        
        return String("Escrow initialized successfully")

    @abimethod()
    def fund_escrow(self) -> String:

        assert Txn.sender == self.client.value, "Only client can fund"
        assert self.status.value == UInt64(1), "Escrow not active"
        
        return String("Escrow funded")

    @abimethod()
    def release_payment(self, amount: UInt64) -> String:

        assert Txn.sender == self.client.value, "Only client can release"
        assert self.status.value == UInt64(1), "Escrow not active"
        assert self.released_amount.value + amount <= self.total_amount.value, "Amount exceeds total"
        
        itxn.Payment(
            receiver=self.freelancer.value,
            amount=amount,
        ).submit()
        
        self.released_amount.value = self.released_amount.value + amount
        
        if self.released_amount.value >= self.total_amount.value:
            self.status.value = UInt64(2)
            return String("Escrow completed - all funds released")
        
        return String("Payment released")

    @abimethod()
    def cancel_escrow(self) -> String:

        assert Txn.sender == self.client.value, "Only client can cancel"
        assert self.status.value == UInt64(1), "Escrow not active"
        assert self.released_amount.value == UInt64(0), "Cannot cancel after release"
        
        self.status.value = UInt64(3)
        return String("Escrow cancelled")

    @abimethod(readonly=True)
    def get_info(self) -> tuple[Account, Account, UInt64, UInt64, UInt64]:

        return (
            self.client.value,
            self.freelancer.value,
            self.total_amount.value,
            self.released_amount.value,
            self.status.value,
        )
