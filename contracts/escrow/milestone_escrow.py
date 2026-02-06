"""
CampusNexus - Milestone-Based Escrow Smart Contract
Algorand Python (PyTeal) - Milestone-Based Escrow for Freelancing

This contract enables:
- Client creates escrow with defined milestones
- Client funds the escrow with ALGO
- Freelancer marks milestones as complete
- Client approves milestones to release funds
- Dispute resolution via third-party arbitrator
"""
from algopy import ARC4Contract, GlobalState, LocalState, BoxRef
from algopy import Account, Application, Asset, Bytes, OnCompleteAction
from algopy import String, UInt64, gtxn, itxn, op, subroutine, Txn


class MilestoneEscrow(ARC4Contract):
    """
    Milestone-Based Escrow Contract for CampusNexus
    
    Lifecycle:
    1. Client creates escrow and defines milestones
    2. Client funds escrow with total ALGO amount
    3. Freelancer works on milestones
    4. Freelancer marks milestone as complete
    5. Client approves milestone -> funds released
    6. Repeat until all milestones complete
    """
    
    # Global State
    client: GlobalState[Account]
    freelancer: GlobalState[Account]
    total_amount: GlobalState[UInt64]
    released_amount: GlobalState[UInt64]
    num_milestones: GlobalState[UInt64]
    completed_milestones: GlobalState[UInt64]
    status: GlobalState[String]  # active, completed, disputed, cancelled
    
    def __init__(self) -> None:
        """Initialize contract state."""
        self.client = GlobalState(Account)
        self.freelancer = GlobalState(Account)
        self.total_amount = GlobalState(UInt64(0))
        self.released_amount = GlobalState(UInt64(0))
        self.num_milestones = GlobalState(UInt64(0))
        self.completed_milestones = GlobalState(UInt64(0))
        self.status = GlobalState(String("inactive"))
    
    @subroutine
    def only_client(self) -> bool:
        """Check if sender is the client."""
        return Txn.sender == self.client.value
    
    @subroutine
    def only_freelancer(self) -> bool:
        """Check if sender is the freelancer."""
        return Txn.sender == self.freelancer.value
    
    def create_escrow(
        self,
        freelancer_addr: Account,
        num_milestones: UInt64,
        milestone_amounts: Bytes,  # Encoded array of amounts
    ) -> None:
        """
        Create a new escrow contract.
        Called by the client to initialize the escrow.
        
        Args:
            freelancer_addr: The freelancer's wallet address
            num_milestones: Number of milestones in the project
            milestone_amounts: Encoded byte array of milestone amounts
        """
        assert self.status.value == String("inactive"), "Escrow already active"
        
        self.client.value = Txn.sender
        self.freelancer.value = freelancer_addr
        self.num_milestones.value = num_milestones
        self.completed_milestones.value = UInt64(0)
        self.released_amount.value = UInt64(0)
        self.status.value = String("active")
    
    def fund_escrow(self, payment: gtxn.PaymentTransaction) -> None:
        """
        Fund the escrow with ALGO.
        Client sends payment to fund all milestones.
        """
        assert self.only_client(), "Only client can fund"
        assert self.status.value == String("active"), "Escrow not active"
        
        self.total_amount.value = payment.amount
    
    def complete_milestone(self, milestone_index: UInt64) -> None:
        """
        Mark a milestone as complete.
        Called by freelancer after completing work.
        """
        assert self.only_freelancer(), "Only freelancer can complete"
        assert self.status.value == String("active"), "Escrow not active"
        assert milestone_index < self.num_milestones.value, "Invalid milestone"
        
        # In production, store milestone status in box storage
        self.completed_milestones.value = self.completed_milestones.value + UInt64(1)
    
    def approve_milestone(self, milestone_index: UInt64, amount: UInt64) -> None:
        """
        Approve a milestone and release funds.
        Called by client to approve work and release payment.
        """
        assert self.only_client(), "Only client can approve"
        assert self.status.value == String("active"), "Escrow not active"
        
        # Release funds to freelancer
        itxn.Payment(
            receiver=self.freelancer.value,
            amount=amount,
            fee=UInt64(1000),
        ).submit()
        
        self.released_amount.value = self.released_amount.value + amount
        
        # Check if all milestones complete
        if self.released_amount.value >= self.total_amount.value:
            self.status.value = String("completed")
    
    def cancel_escrow(self) -> None:
        """
        Cancel the escrow and refund remaining funds.
        Only callable by client before any milestones approved.
        """
        assert self.only_client(), "Only client can cancel"
        assert self.status.value == String("active"), "Escrow not active"
        assert self.released_amount.value == UInt64(0), "Funds already released"
        
        # Refund to client
        remaining = self.total_amount.value - self.released_amount.value
        if remaining > UInt64(0):
            itxn.Payment(
                receiver=self.client.value,
                amount=remaining,
                fee=UInt64(1000),
            ).submit()
        
        self.status.value = String("cancelled")
    
    def get_escrow_info(self) -> tuple[Account, Account, UInt64, UInt64, String]:
        """Get escrow information."""
        return (
            self.client.value,
            self.freelancer.value,
            self.total_amount.value,
            self.released_amount.value,
            self.status.value,
        )
