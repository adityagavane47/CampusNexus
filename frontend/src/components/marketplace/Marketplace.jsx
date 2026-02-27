import { useState, useEffect } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';
import { useEscrow } from '../../hooks/useEscrow';
import { CreateListingModal } from './CreateListingModal';

const API_BASE = 'http://localhost:8000/api';

const categories = [
    { id: 'all', name: 'All' },
    { id: 'arduino', name: 'Arduino' },
    { id: 'books', name: 'Books' },
    { id: 'laptops', name: 'Laptops' },
    { id: 'components', name: 'Components' },
];

export function Marketplace() {
    const { isConnected, accountAddress, signTransaction } = usePeraWallet();
    const { createEscrow, fundEscrow, isLoading: escrowLoading } = useEscrow();
    const [listings, setListings] = useState([]);
    const [activeCategory, setActiveCategory] = useState('all');
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [loading, setLoading] = useState(true);
    const [purchasingItemId, setPurchasingItemId] = useState(null);
    const [purchaseStatus, setPurchaseStatus] = useState('');

    useEffect(() => {
        fetchListings();
    }, []);

    const fetchListings = async () => {
        try {
            const response = await fetch(`${API_BASE}/marketplace/`);
            if (response.ok) {
                const data = await response.json();
                setListings(data);
            }
        } catch (error) {
            console.error('Failed to fetch listings:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePurchase = async (listing) => {
        if (!isConnected || !accountAddress) {
            alert('❌ Please connect your wallet first');
            return;
        }

        setPurchasingItemId(listing.id);
        setPurchaseStatus('Initiating purchase...');

        try {
            setPurchaseStatus('Calling backend...');
            const response = await fetch(`${API_BASE}/marketplace/${listing.id}/purchase`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ buyer_address: accountAddress }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Purchase initiation failed');
            }

            const data = await response.json();
            const { seller_address, escrow_required } = data;

            setPurchaseStatus('Creating escrow contract...');
            const escrowResult = await createEscrow(
                accountAddress,
                signTransaction,
                seller_address,
                escrow_required,
                1
            );

            if (!escrowResult) {
                throw new Error('Escrow creation failed');
            }

            setPurchaseStatus('');
            setPurchasingItemId(null);
            alert(`✅ Purchase successful!\n\nItem: ${listing.title}\nAmount: ${escrow_required} ALGO\n\nEscrow contract created.`);
            fetchListings();
        } catch (error) {
            console.error('Purchase error:', error);
            setPurchaseStatus('');
            setPurchasingItemId(null);
            alert(`❌ Purchase failed:\n${error.message}`);
            fetchListings();
        }
    };

    const filteredListings = activeCategory === 'all'
        ? listings
        : listings.filter(l => l.category === activeCategory);

    return (
        <div className="animate-fade-in">
            <div className="section-header">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h2 className="section-title">Marketplace</h2>
                        <p style={{ color: 'var(--text-secondary)' }}>
                            Buy & sell electronics, books, and more
                        </p>
                    </div>
                    <button
                        onClick={() => setShowCreateModal(true)}
                        className="btn-primary"
                        style={{ padding: '12px 24px' }}
                    >
                        + Create Listing
                    </button>
                </div>

                <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
                    {categories.map(cat => (
                        <button
                            key={cat.id}
                            onClick={() => setActiveCategory(cat.id)}
                            className={activeCategory === cat.id ? 'tag tag-dark' : 'tag'}
                            style={{ cursor: 'pointer', border: 'none' }}
                        >
                            {cat.name}
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div style={{ textAlign: 'center', padding: '80px', color: 'var(--text-muted)' }}>
                    <div style={{
                        width: '40px', height: '40px',
                        border: '2px solid var(--border-subtle)',
                        borderTopColor: 'var(--accent-teal)',
                        borderRadius: '50%',
                        animation: 'rotate 0.8s linear infinite',
                        margin: '0 auto 16px',
                    }} />
                    Loading marketplace...
                </div>
            ) : (
                <div className="grid-3">
                    {filteredListings.length === 0 ? (
                        <div className="card" style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '64px' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '16px', filter: 'drop-shadow(0 0 12px rgba(0,212,170,0.3))' }}>📦</div>
                            <h3 style={{ marginBottom: '8px' }}>No listings yet</h3>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Be the first to list an item!</p>
                        </div>
                    ) : (
                        filteredListings.map((listing) => (
                            <div key={listing.id} className="product-card">
                                <div className="product-image">
                                    {listing.ipfs_cid ? (
                                        <img
                                            src={`https://gateway.pinata.cloud/ipfs/${listing.ipfs_cid}`}
                                            alt={listing.title}
                                            style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }}
                                        />
                                    ) : (
                                        <span style={{ fontSize: '3rem' }}>📦</span>
                                    )}
                                </div>
                                <div className="product-info">
                                    <h3 className="product-title">{listing.title}</h3>
                                    <p className="product-price">{listing.price_algo} ALGO</p>
                                    <div style={{ marginTop: '12px' }}>
                                        <button
                                            className="btn-secondary"
                                            style={{
                                                width: '100%',
                                                padding: '10px',
                                                opacity: purchasingItemId === listing.id ? 0.7 : 1,
                                                cursor: purchasingItemId === listing.id ? 'wait' : 'pointer'
                                            }}
                                            onClick={() => handlePurchase(listing)}
                                            disabled={purchasingItemId === listing.id}
                                        >
                                            {purchasingItemId === listing.id
                                                ? `⏳ ${purchaseStatus}`
                                                : 'Purchase'}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}

            
            {showCreateModal && (
                <CreateListingModal
                    onClose={() => setShowCreateModal(false)}
                    onSuccess={() => {
                        fetchListings();
                        alert('✅ Listing created successfully!');
                    }}
                />
            )}
        </div>
    );
}

export default Marketplace;
