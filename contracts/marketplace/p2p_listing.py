from algopy import ARC4Contract, GlobalState
from algopy import Account, Bytes, String, UInt64, gtxn, itxn, Txn

class P2PListing(ARC4Contract):

    seller: GlobalState[Account]
    buyer: GlobalState[Account]
    price: GlobalState[UInt64]
    title: GlobalState[String]
    category: GlobalState[String]
    ipfs_cid: GlobalState[String]
    status: GlobalState[String]
    
    def __init__(self) -> None:

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

        assert self.status.value == String("inactive"), "Listing already exists"
        
        self.seller.value = Txn.sender
        self.title.value = title
        self.category.value = category
        self.price.value = price_microalgos
        self.ipfs_cid.value = ipfs_cid
        self.status.value = String("listed")
    
    def purchase(self, payment: gtxn.PaymentTransaction) -> None:

        assert self.status.value == String("listed"), "Item not available"
        assert payment.amount >= self.price.value, "Insufficient payment"
        assert Txn.sender != self.seller.value, "Seller cannot buy own item"
        
        self.buyer.value = Txn.sender
        self.status.value = String("pending")
    
    def confirm_receipt(self) -> None:

        assert Txn.sender == self.buyer.value, "Only buyer can confirm"
        assert self.status.value == String("pending"), "No pending purchase"
        
        itxn.Payment(
            receiver=self.seller.value,
            amount=self.price.value,
            fee=UInt64(1000),
        ).submit()
        
        
        self.status.value = String("sold")
    
    def cancel_listing(self) -> None:

        assert Txn.sender == self.seller.value, "Only seller can cancel"
        assert self.status.value == String("listed"), "Cannot cancel"
        
        self.status.value = String("cancelled")
    
    def refund_buyer(self) -> None:

        assert self.status.value == String("pending"), "No pending purchase"
        
        itxn.Payment(
            receiver=self.buyer.value,
            amount=self.price.value,
            fee=UInt64(1000),
        ).submit()
        
        self.status.value = String("cancelled")
    
    def get_listing_info(self) -> tuple[Account, String, String, UInt64, String, String]:

        return (
            self.seller.value,
            self.title.value,
            self.category.value,
            self.price.value,
            self.ipfs_cid.value,
            self.status.value,
        )
