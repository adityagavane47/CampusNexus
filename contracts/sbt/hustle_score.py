from algopy import ARC4Contract, GlobalState, BoxRef
from algopy import Account, Bytes, String, UInt64, Txn, op

class HustleScoreSBT(ARC4Contract):

    admin: GlobalState[Account]
    total_tokens_minted: GlobalState[UInt64]
    
    def __init__(self) -> None:

        self.admin = GlobalState(Account)
        self.total_tokens_minted = GlobalState(UInt64(0))
    
    def initialize(self) -> None:

        self.admin.value = Txn.sender
        self.total_tokens_minted.value = UInt64(0)
    
    def mint_sbt(self, student_address: Account) -> UInt64:

        assert Txn.sender == self.admin.value, "Only admin can mint"
        
        token_id = self.total_tokens_minted.value + UInt64(1)
        self.total_tokens_minted.value = token_id
        
        
        return token_id
    
    def add_project_completion(
        self, 
        student: Account, 
        project_budget_algos: UInt64
    ) -> UInt64:

        assert Txn.sender == self.admin.value, "Only admin can update"
        
        points = UInt64(10)
        if project_budget_algos >= UInt64(100_000_000):
            points = UInt64(50)
        elif project_budget_algos >= UInt64(50_000_000):
            points = UInt64(40)
        elif project_budget_algos >= UInt64(25_000_000):
            points = UInt64(25)
        
        return points
    
    def add_endorsement(
        self, 
        student: Account, 
        endorser: Account, 
        skill: String
    ) -> None:

        assert endorser != student, "Cannot endorse yourself"
    
    def add_dispute_penalty(self, student: Account) -> None:

        assert Txn.sender == self.admin.value, "Only admin can penalize"
    
    def get_hustle_score(self, student: Account) -> UInt64:

        return UInt64(100)
    
    def get_student_stats(
        self, 
        student: Account
    ) -> tuple[UInt64, UInt64, UInt64, UInt64]:

        return (UInt64(100), UInt64(0), UInt64(0), UInt64(0))
