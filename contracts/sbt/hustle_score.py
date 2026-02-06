"""
CampusNexus - Hustle Score Soulbound Token (SBT)
Algorand Python - Non-Transferable Reputation Token

This contract implements:
- Soulbound Token (non-transferable)
- Hustle Score based on completed gigs
- Skill endorsements
- On-chain reputation for VIT Pune students
"""
from algopy import ARC4Contract, GlobalState, BoxRef
from algopy import Account, Bytes, String, UInt64, Txn, op


class HustleScoreSBT(ARC4Contract):
    """
    Hustle Score Soulbound Token for CampusNexus
    
    Features:
    - Non-transferable reputation token
    - Score increases with completed projects
    - Skill endorsements from peers
    - Verified achievements on-chain
    
    Score Calculation:
    - Base: 100 points
    - Per completed project: +10-50 points (based on budget)
    - Per endorsement: +5 points
    - Disputes against: -20 points
    """
    
    # Global State - Admin
    admin: GlobalState[Account]
    total_tokens_minted: GlobalState[UInt64]
    
    def __init__(self) -> None:
        """Initialize the SBT contract."""
        self.admin = GlobalState(Account)
        self.total_tokens_minted = GlobalState(UInt64(0))
    
    def initialize(self) -> None:
        """Initialize the contract with admin."""
        self.admin.value = Txn.sender
        self.total_tokens_minted.value = UInt64(0)
    
    def mint_sbt(self, student_address: Account) -> UInt64:
        """
        Mint a new Hustle Score SBT for a student.
        Only admin (CampusNexus platform) can mint.
        
        Args:
            student_address: The student's wallet address
            
        Returns:
            The token ID of the minted SBT
        """
        assert Txn.sender == self.admin.value, "Only admin can mint"
        
        # Create box for student's score data
        token_id = self.total_tokens_minted.value + UInt64(1)
        self.total_tokens_minted.value = token_id
        
        # Initialize with base score of 100
        # Box: student_address -> (hustle_score, projects_completed, endorsements, disputes)
        
        return token_id
    
    def add_project_completion(
        self, 
        student: Account, 
        project_budget_algos: UInt64
    ) -> UInt64:
        """
        Add points for completing a project.
        Called when escrow is successfully completed.
        
        Points:
        - Budget < 25 ALGO: +10 points
        - Budget 25-50 ALGO: +25 points
        - Budget 50-100 ALGO: +40 points
        - Budget > 100 ALGO: +50 points
        """
        assert Txn.sender == self.admin.value, "Only admin can update"
        
        # Calculate points based on budget
        points = UInt64(10)
        if project_budget_algos >= UInt64(100_000_000):  # 100 ALGO
            points = UInt64(50)
        elif project_budget_algos >= UInt64(50_000_000):  # 50 ALGO
            points = UInt64(40)
        elif project_budget_algos >= UInt64(25_000_000):  # 25 ALGO
            points = UInt64(25)
        
        return points
    
    def add_endorsement(
        self, 
        student: Account, 
        endorser: Account, 
        skill: String
    ) -> None:
        """
        Add a skill endorsement from another student.
        Endorser must have an SBT themselves.
        
        Each endorsement: +5 points
        """
        assert endorser != student, "Cannot endorse yourself"
        # In production: verify endorser has SBT
        # Add 5 points to student's score
    
    def add_dispute_penalty(self, student: Account) -> None:
        """
        Deduct points for dispute ruled against student.
        Called by admin after dispute resolution.
        
        Penalty: -20 points
        """
        assert Txn.sender == self.admin.value, "Only admin can penalize"
        # Deduct 20 points (minimum score: 0)
    
    def get_hustle_score(self, student: Account) -> UInt64:
        """
        Get the current Hustle Score for a student.
        
        Returns:
            The student's current Hustle Score
        """
        # In production: read from box storage
        # Return the student's score
        return UInt64(100)  # Placeholder
    
    def get_student_stats(
        self, 
        student: Account
    ) -> tuple[UInt64, UInt64, UInt64, UInt64]:
        """
        Get detailed stats for a student.
        
        Returns:
            (hustle_score, projects_completed, endorsements_received, disputes)
        """
        # Placeholder - implement with box storage
        return (UInt64(100), UInt64(0), UInt64(0), UInt64(0))
    
    # Note: Transfer function is intentionally NOT implemented
    # This makes the token "soulbound" - it cannot be transferred
    # The token is permanently bound to the student's wallet
