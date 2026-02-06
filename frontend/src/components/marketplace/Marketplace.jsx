/**
 * CampusNexus - Marketplace Component (Minimalist Design)
 */
import { useState } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

const mockListings = [
    {
        id: 1,
        title: "Arduino Uno R3 Kit",
        category: "arduino",
        price_algo: 15,
        seller: "VIT3...K8M2",
        image: "🔌"
    },
    {
        id: 2,
        title: "Algorithms Book",
        category: "books",
        price_algo: 8,
        seller: "VIT7...P4N1",
        image: "📚"
    },
    {
        id: 3,
        title: "Raspberry Pi 4",
        category: "electronics",
        price_algo: 25,
        seller: "VIT1...Q9L5",
        image: "💻"
    },
    {
        id: 4,
        title: "Jumper Wires Set",
        category: "components",
        price_algo: 2,
        seller: "VIT9...L2K1",
        image: "🔧"
    },
];

const categories = [
    { id: 'all', name: 'All' },
    { id: 'arduino', name: 'Arduino' },
    { id: 'books', name: 'Books' },
    { id: 'electronics', name: 'Electronics' },
];

export function Marketplace() {
    const { isConnected } = usePeraWallet();
    const [activeCategory, setActiveCategory] = useState('all');

    const filteredListings = activeCategory === 'all'
        ? mockListings
        : mockListings.filter(l => l.category === activeCategory);

    return (
        <div className="animate-fade-in">
            <div className="section-header">
                <h2 className="section-title">Marketplace</h2>
                <div style={{ display: 'flex', gap: '8px' }}>
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

            <div className="grid-3">
                {filteredListings.map((listing) => (
                    <div key={listing.id} className="product-card">
                        <div className="product-image">
                            <span style={{ fontSize: '3rem' }}>{listing.image}</span>
                        </div>
                        <div className="product-info">
                            <h3 className="product-title">{listing.title}</h3>
                            <p className="product-price">{listing.price_algo} ALGO</p>
                            <div style={{ marginTop: '12px' }}>
                                <button
                                    className="btn-secondary"
                                    style={{ width: '100%', padding: '10px' }}
                                    onClick={() => alert(`Buying ${listing.title}`)}
                                >
                                    Purchase
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Marketplace;
