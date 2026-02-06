"""
CampusNexus - Milestone-Based Escrow Smart Contract
For student freelancing on Algorand
"""
from algopy import ARC4Contract, GlobalState, UInt64, Account, String, Txn, itxn
from algopy.arc4 import abimethod


class MilestoneEscrow(ARC4Contract):
    """
    Milestone-Based Escrow for CampusNexus
    
    Flow:
    1. Client creates escrow and defines total amount
    2. Client funds the escrow
    3. Freelancer marks work complete
    4. Client approves and funds release
    """
    
    def __init__(self) -> None:
        self.client = GlobalState(Account)
        self.freelancer = GlobalState(Account)
        self.total_amount = GlobalState(UInt64(0))
        self.released_amount = GlobalState(UInt64(0))
        self.status = GlobalState(UInt64(0))  # 0=inactive, 1=active, 2=completed, 3=cancelled

    @abimethod()
    def create_escrow(self, freelancer_addr: Account, amount: UInt64) -> String:
        """Create a new escrow contract."""
        assert self.status.value == UInt64(0), "Escrow already exists"
        
        self.client.value = Txn.sender
        self.freelancer.value = freelancer_addr
        self.total_amount.value = amount
        self.released_amount.value = UInt64(0)
        self.status.value = UInt64(1)
        
        return String("Escrow created successfully")

    @abimethod()
    def fund_escrow(self) -> String:
        """Fund the escrow (client sends ALGO)."""
        assert Txn.sender == self.client.value, "Only client can fund"
        assert self.status.value == UInt64(1), "Escrow not active"
        
        return String("Escrow funded")

    @abimethod()
    def release_payment(self, amount: UInt64) -> String:
        """Release payment to freelancer (called by client)."""
        assert Txn.sender == self.client.value, "Only client can release"
        assert self.status.value == UInt64(1), "Escrow not active"
        assert self.released_amount.value + amount <= self.total_amount.value, "Amount exceeds total"
        
        # Transfer to freelancer
        itxn.Payment(
            receiver=self.freelancer.value,
            amount=amount,
        ).submit()
        
        self.released_amount.value = self.released_amount.value + amount
        
        # Check if fully released
        if self.released_amount.value >= self.total_amount.value:
            self.status.value = UInt64(2)  # completed
            return String("Escrow completed - all funds released")
        
        return String("Payment released")

    @abimethod()
    def cancel_escrow(self) -> String:
        """Cancel escrow and refund client."""
        assert Txn.sender == self.client.value, "Only client can cancel"
        assert self.status.value == UInt64(1), "Escrow not active"
        assert self.released_amount.value == UInt64(0), "Cannot cancel after release"
        
        self.status.value = UInt64(3)  # cancelled
        return String("Escrow cancelled")

    @abimethod(readonly=True)
    def get_info(self) -> tuple[Account, Account, UInt64, UInt64, UInt64]:
        """Get escrow information."""
        return (
            self.client.value,
            self.freelancer.value,
            self.total_amount.value,
            self.released_amount.value,
            self.status.value,
        )
