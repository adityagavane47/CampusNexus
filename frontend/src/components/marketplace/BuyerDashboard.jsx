import { useState, useEffect } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

const API_BASE = 'http://localhost:8000/api';

export function BuyerDashboard() {
    const { accountAddress, sendTransaction } = usePeraWallet();
    const [purchases, setPurchases] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (accountAddress) {
            fetchPurchases();
        }
    }, [accountAddress]);

    const fetchPurchases = async () => {
        try {
            const mockPurchases = [
                {
                    id: 1,
                    title: "Arduino Uno R3 Kit",
                    price_algo: 15,
                    seller_address: "VIT3...K8M2",
                    status: "pending",
                    ipfs_cid: "QmTest123",
                    purchased_at: new Date().toISOString()
                }
            ];
            setPurchases(mockPurchases);
        } catch (error) {
            console.error('Failed to fetch purchases:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleConfirmReceipt = async (listingId) => {
        if (!confirm('Have you received the item? This will release funds to the seller.')) {
            return;
        }

        try {

            await fetch(`${API_BASE}/marketplace/${listingId}/confirm`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ buyer_address: accountAddress })
            });

            fetchPurchases();

            alert('✅ Receipt confirmed! Funds released to seller.');
        } catch (error) {
            console.error('Confirmation error:', error);
            alert('Failed to confirm receipt. Please try again.');
        }
    };

    if (loading) {
        return <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>;
    }

    return (
        <div className="animate-fade-in">
            <div className="section-header">
                <h2 className="section-title">My Purchases</h2>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Track your orders and confirm receipt
                </p>
            </div>

            {purchases.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '60px' }}>
                    <p style={{ fontSize: '3rem', marginBottom: '16px' }}>📦</p>
                    <h3>No purchases yet</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        Browse the marketplace to find items
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '24px' }}>
                    {purchases.map(purchase => (
                        <div key={purchase.id} className="card" style={{ padding: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
                                        
                                        <div style={{
                                            width: '80px',
                                            height: '80px',
                                            background: 'var(--bg-secondary)',
                                            borderRadius: '8px',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            fontSize: '2rem'
                                        }}>
                                            {purchase.ipfs_cid ? '🖼️' : '📦'}
                                        </div>

                                        
                                        <div style={{ flex: 1 }}>
                                            <h3 style={{ margin: '0 0 8px 0' }}>{purchase.title}</h3>
                                            <p style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>
                                                Seller: {purchase.seller_address}
                                            </p>
                                            <p style={{ fontWeight: '600', fontSize: '1.25rem' }}>
                                                {purchase.price_algo} ALGO
                                            </p>
                                        </div>
                                    </div>

                                    
                                    <div style={{ marginBottom: '16px' }}>
                                        {purchase.status === 'pending' ? (
                                            <span className="tag" style={{ background: 'var(--accent-yellow)', color: '#000' }}>
                                                ⏳ Awaiting Confirmation
                                            </span>
                                        ) : (
                                            <span className="tag tag-dark">
                                                ✅ Confirmed
                                            </span>
                                        )}
                                    </div>

                                    
                                    {purchase.status === 'pending' && (
                                        <div>
                                            <button
                                                onClick={() => handleConfirmReceipt(purchase.id)}
                                                className="btn-primary"
                                                style={{ padding: '12px 24px' }}
                                            >
                                                ✅ Confirm Receipt
                                            </button>
                                            <p style={{ marginTop: '8px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                                Click after you receive the item to release funds
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default BuyerDashboard;
