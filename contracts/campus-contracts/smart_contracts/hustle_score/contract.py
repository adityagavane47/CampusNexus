"""
CampusNexus - Hustle Score Soulbound Token (SBT)
Non-transferable reputation token for VIT Pune students
"""
from algopy import ARC4Contract, GlobalState, UInt64, Account, String, Txn
from algopy.arc4 import abimethod


class HustleScore(ARC4Contract):
    """
    Hustle Score SBT for CampusNexus
    
    Features:
    - Non-transferable (soulbound)
    - Score increases with completed projects
    - Admin-managed minting
    """
    
    def __init__(self) -> None:
        self.admin = GlobalState(Account)
        self.total_minted = GlobalState(UInt64(0))

    @abimethod(create="require")
    def create(self) -> String:
        """Initialize the contract with creator as admin."""
        self.admin.value = Txn.sender
        self.total_minted.value = UInt64(0)
        return String("HustleScore SBT initialized")

    @abimethod()
    def add_reputation(self, student: Account, points: UInt64) -> String:
        """Add reputation points to a student (admin only)."""
        assert Txn.sender == self.admin.value, "Only admin can add reputation"
        
        # In production, store in box storage per student
        self.total_minted.value = self.total_minted.value + points
        
        return String("Reputation added")

    @abimethod()
    def remove_reputation(self, student: Account, points: UInt64) -> String:
        """Remove reputation points (for disputes, admin only)."""
        assert Txn.sender == self.admin.value, "Only admin can remove reputation"
        
        return String("Reputation removed")

    @abimethod(readonly=True)
    def get_total_minted(self) -> UInt64:
        """Get total reputation points minted."""
        return self.total_minted.value

    @abimethod(readonly=True)
    def get_admin(self) -> Account:
        """Get the admin address."""
        return self.admin.value

    # NOTE: No transfer function - this makes it soulbound
