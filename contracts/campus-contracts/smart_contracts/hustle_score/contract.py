from algopy import ARC4Contract, GlobalState, BoxMap, Account, String, Txn, UInt64
from algopy.arc4 import abimethod, baremethod, UInt64 as ARC4UInt64

class HustleScore(ARC4Contract):

    def __init__(self) -> None:
        self.admin = GlobalState(Account)
        self.scores = BoxMap(Account, UInt64)

    @abimethod(create="require")
    def create(self) -> String:

        self.admin.value = Txn.sender
        return String("HustleScore SBT initialized")
    
    @baremethod(create="allow", allow_actions=["NoOp", "UpdateApplication", "DeleteApplication"])
    def bare_routing(self) -> None:

        self.admin.value = Txn.sender

    @abimethod()
    def mint_initial(self, student: Account) -> String:

        assert Txn.sender == self.admin.value, "Only admin can mint"
        
        exists, _val = self.scores.maybe(student)
        assert not exists, "Student already initialized"
        
        self.scores[student] = UInt64(0)
        
        return String("Student initialized with 0 score")

    @abimethod()
    def add_reputation(self, student: Account, points: UInt64) -> String:

        assert Txn.sender == self.admin.value, "Only admin can add reputation"
        
        exists, current_score = self.scores.maybe(student)
        assert exists, "Student not initialized"
        
        self.scores[student] = current_score + points
        
        return String("Reputation added")

    @abimethod(readonly=True)
    def get_score(self, student: Account) -> ARC4UInt64:

        exists, score = self.scores.maybe(student)
        if not exists:
            return ARC4UInt64(UInt64(0))
        
        return ARC4UInt64(score)

    @abimethod(readonly=True)
    def get_admin(self) -> Account:

        return self.admin.value
