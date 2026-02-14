"""
CampusNexus - Hustle Score Soulbound Token (SBT)
Non-transferable reputation token for VIT Pune students
Uses Box Storage (BoxMap) for individual student scores
"""
from algopy import ARC4Contract, GlobalState, BoxMap, Account, String, Txn, UInt64
from algopy.arc4 import abimethod, baremethod, UInt64 as ARC4UInt64


class HustleScore(ARC4Contract):
    """
    Hustle Score SBT for CampusNexus
    
    Features:
    - Non-transferable (soulbound)
    - Per-student score stored in BoxMap
    - Score increases with completed projects
    - Admin-managed score updates
    """
    
    def __init__(self) -> None:
        self.admin = GlobalState(Account)
        self.scores = BoxMap(Account, UInt64)

    @abimethod(create="require")
    def create(self) -> String:
        """Initialize the contract with creator as admin."""
        self.admin.value = Txn.sender
        return String("HustleScore SBT initialized")
    
    @baremethod(create="allow", allow_actions=["NoOp", "UpdateApplication", "DeleteApplication"])
    def bare_routing(self) -> None:
        """Handle bare actions: Create (NoOp), Update, Delete."""
        # During creation, admin is set. For update/delete, we allow (commented out admin check for now)
        # No explicit check needed - algopy routing handles ApplicationID semantics
        self.admin.value = Txn.sender

    @abimethod()
    def mint_initial(self, student: Account) -> String:
        """Initialize a student with 0 score (creates box storage)."""
        assert Txn.sender == self.admin.value, "Only admin can mint"
        
        # Check if already exists
        exists, _val = self.scores.maybe(student)
        assert not exists, "Student already initialized"
        
        # Initialize with 0
        self.scores[student] = UInt64(0)
        
        return String("Student initialized with 0 score")

    @abimethod()
    def add_reputation(self, student: Account, points: UInt64) -> String:
        """Add reputation points to a student (admin only)."""
        assert Txn.sender == self.admin.value, "Only admin can add reputation"
        
        # Ensure student is initialized
        exists, current_score = self.scores.maybe(student)
        assert exists, "Student not initialized"
        
        # Update score
        self.scores[student] = current_score + points
        
        return String("Reputation added")

    @abimethod(readonly=True)
    def get_score(self, student: Account) -> ARC4UInt64:
        """Get reputation score for a student."""
        exists, score = self.scores.maybe(student)
        if not exists:
            return ARC4UInt64(UInt64(0))
        
        return ARC4UInt64(score)

    @abimethod(readonly=True)
    def get_admin(self) -> Account:
        """Get the admin address."""
        return self.admin.value

    # NOTE: No transfer function - this makes it soulbound


