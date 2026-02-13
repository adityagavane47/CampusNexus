"""
CampusNexus - P2P Marketplace Smart Contract
Algorand Python - Escrow-Protected Peer-to-Peer Listings

This contract enables:
- Sellers list items (Arduino kits, books, electronics)
- Buyers can purchase with escrow protection
- Automatic release on confirmation
- Dispute resolution mechanism
"""
from algopy import ARC4Contract, GlobalState
from algopy import Account, Bytes, String, UInt64, gtxn, itxn, Txn


class P2PListing(ARC4Contract):
    """
    P2P Marketplace Listing Contract for CampusNexus
    
    Lifecycle:
    1. Seller creates listing with price and details
    2. Buyer initiates purchase (funds held in escrow)
    3. Seller delivers item
    4. Buyer confirms receipt -> funds released
    5. Or dispute raised -> arbitration
    """
    
    # Global State
    seller: GlobalState[Account]
    buyer: GlobalState[Account]
    price: GlobalState[UInt64]
    title: GlobalState[String]
    category: GlobalState[String]
    ipfs_cid: GlobalState[String]  # IPFS Content Identifier for item images
    status: GlobalState[String]  # listed, pending, sold, disputed, cancelled
    
    def __init__(self) -> None:
        """Initialize listing state."""
        self.seller = GlobalState(Account)
        self.buyer = GlobalState(Account)
        self.price = GlobalState(UInt64(0))
        self.title = GlobalState(String(""))
        self.category = GlobalState(String(""))
        self.ipfs_cid = GlobalState(String(""))
        self.status = GlobalState(String("inactive"))
    
    def create_listing(
        self,
        title: String,
        category: String,
        price_microalgos: UInt64,
        ipfs_cid: String,
    ) -> None:
        """
        Create a new marketplace listing.
        
        Args:
            title: Item title
            category: Category (arduino, books, electronics, etc.)
            price_microalgos: Price in microALGOs
            ipfs_cid: IPFS Content Identifier for item image
        """
        assert self.status.value == String("inactive"), "Listing already exists"
        
        self.seller.value = Txn.sender
        self.title.value = title
        self.category.value = category
        self.price.value = price_microalgos
        self.ipfs_cid.value = ipfs_cid
        self.status.value = String("listed")
    
    def purchase(self, payment: gtxn.PaymentTransaction) -> None:
        """
        Initiate purchase of the item.
        Buyer sends payment which is held in escrow.
        """
        assert self.status.value == String("listed"), "Item not available"
        assert payment.amount >= self.price.value, "Insufficient payment"
        assert Txn.sender != self.seller.value, "Seller cannot buy own item"
        
        self.buyer.value = Txn.sender
        self.status.value = String("pending")
    
    def confirm_receipt(self) -> None:
        """
        Buyer confirms item receipt.
        Releases escrowed funds to seller and awards reputation badge.
        """
        assert Txn.sender == self.buyer.value, "Only buyer can confirm"
        assert self.status.value == String("pending"), "No pending purchase"
        
        # Release funds to seller
        itxn.Payment(
            receiver=self.seller.value,
            amount=self.price.value,
            fee=UInt64(1000),
        ).submit()
        
        # Award "Trusted Trader" badge to seller via HustleScore contract
        # Note: Requires HUSTLE_SCORE_APP_ID to be set at deployment
        # For now, this is commented out - will be enabled when HustleScore is deployed
        # itxn.ApplicationCall(
        #     app_id=UInt64(HUSTLE_SCORE_APP_ID),
        #     app_args=[Bytes(b"award_badge"), Bytes(b"trusted_trader")],
        #     accounts=[self.seller.value],
        #     fee=UInt64(1000),
        # ).submit()
        
        self.status.value = String("sold")
    
    def cancel_listing(self) -> None:
        """
        Cancel an active listing.
        Only seller can cancel if no pending purchase.
        """
        assert Txn.sender == self.seller.value, "Only seller can cancel"
        assert self.status.value == String("listed"), "Cannot cancel"
        
        self.status.value = String("cancelled")
    
    def refund_buyer(self) -> None:
        """
        Refund buyer if dispute resolved in their favor.
        """
        assert self.status.value == String("pending"), "No pending purchase"
        
        # Refund to buyer
        itxn.Payment(
            receiver=self.buyer.value,
            amount=self.price.value,
            fee=UInt64(1000),
        ).submit()
        
        self.status.value = String("cancelled")
    
    def get_listing_info(self) -> tuple[Account, String, String, UInt64, String, String]:
        """Get listing information including IPFS image CID."""
        return (
            self.seller.value,
            self.title.value,
            self.category.value,
            self.price.value,
            self.ipfs_cid.value,
            self.status.value,
        )
