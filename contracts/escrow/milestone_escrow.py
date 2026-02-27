from algopy import ARC4Contract, GlobalState, LocalState, BoxRef
from algopy import Account, Application, Asset, Bytes, OnCompleteAction
from algopy import String, UInt64, gtxn, itxn, op, subroutine, Txn

class MilestoneEscrow(ARC4Contract):

    client: GlobalState[Account]
    freelancer: GlobalState[Account]
    total_amount: GlobalState[UInt64]
    released_amount: GlobalState[UInt64]
    num_milestones: GlobalState[UInt64]
    completed_milestones: GlobalState[UInt64]
    status: GlobalState[String]
    
    def __init__(self) -> None:

        self.client = GlobalState(Account)
        self.freelancer = GlobalState(Account)
        self.total_amount = GlobalState(UInt64(0))
        self.released_amount = GlobalState(UInt64(0))
        self.num_milestones = GlobalState(UInt64(0))
        self.completed_milestones = GlobalState(UInt64(0))
        self.status = GlobalState(String("inactive"))
    
    @subroutine
    def only_client(self) -> bool:

        return Txn.sender == self.client.value
    
    @subroutine
    def only_freelancer(self) -> bool:

        return Txn.sender == self.freelancer.value
    
    def create_escrow(
        self,
        freelancer_addr: Account,
        num_milestones: UInt64,
        milestone_amounts: Bytes,
    ) -> None:

        assert self.status.value == String("inactive"), "Escrow already active"
        
        self.client.value = Txn.sender
        self.freelancer.value = freelancer_addr
        self.num_milestones.value = num_milestones
        self.completed_milestones.value = UInt64(0)
        self.released_amount.value = UInt64(0)
        self.status.value = String("active")
    
    def fund_escrow(self, payment: gtxn.PaymentTransaction) -> None:

        assert self.only_client(), "Only client can fund"
        assert self.status.value == String("active"), "Escrow not active"
        
        self.total_amount.value = payment.amount
    
    def complete_milestone(self, milestone_index: UInt64) -> None:

        assert self.only_freelancer(), "Only freelancer can complete"
        assert self.status.value == String("active"), "Escrow not active"
        assert milestone_index < self.num_milestones.value, "Invalid milestone"
        
        self.completed_milestones.value = self.completed_milestones.value + UInt64(1)
    
    def approve_milestone(self, milestone_index: UInt64, amount: UInt64) -> None:

        assert self.only_client(), "Only client can approve"
        assert self.status.value == String("active"), "Escrow not active"
        assert milestone_index < self.num_milestones.value, "Invalid milestone index"
        
        assert self.released_amount.value + amount <= self.total_amount.value, \
            "Payment exceeds total escrow amount"
        
        itxn.Payment(
            receiver=self.freelancer.value,
            amount=amount,
            fee=UInt64(1000),
        ).submit()
        
        self.released_amount.value = self.released_amount.value + amount
        
        if self.released_amount.value >= self.total_amount.value:
            self.status.value = String("completed")
    
    def cancel_escrow(self) -> None:

        assert self.only_client(), "Only client can cancel"
        assert self.status.value == String("active"), "Escrow not active"
        assert self.released_amount.value == UInt64(0), "Funds already released"
        
        remaining = self.total_amount.value - self.released_amount.value
        if remaining > UInt64(0):
            itxn.Payment(
                receiver=self.client.value,
                amount=remaining,
                fee=UInt64(1000),
            ).submit()
        
        self.status.value = String("cancelled")
    
    def get_escrow_info(self) -> tuple[Account, Account, UInt64, UInt64, String]:

        return (
            self.client.value,
            self.freelancer.value,
            self.total_amount.value,
            self.released_amount.value,
            self.status.value,
        )
