/**
 * CampusNexus - Marketplace Component
 * P2P marketplace for buying/selling equipment
 */
import { useState } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

const mockListings = [
    {
        id: 1,
        title: "Arduino Uno R3 Starter Kit",
        description: "Complete kit with sensors, LEDs, jumper wires. Used for 1 semester only.",
        category: "arduino",
        price_algo: 15,
        condition: "like_new",
        seller_address: "VIT3...K8M2",
        status: "available",
    },
    {
        id: 2,
        title: "Data Structures & Algorithms Book",
        description: "CLRS Introduction to Algorithms, 3rd Edition. Minimal highlighting.",
        category: "books",
        price_algo: 8,
        condition: "good",
        seller_address: "VIT7...P4N1",
        status: "available",
    },
    {
        id: 3,
        title: "Raspberry Pi 4 (4GB RAM)",
        description: "Includes case, power supply, and 32GB SD card. Perfect for projects.",
        category: "electronics",
        price_algo: 25,
        condition: "good",
        seller_address: "VIT1...Q9L5",
        status: "available",
    },
];

const categories = [
    { id: 'all', name: 'All Items', icon: '📦' },
    { id: 'arduino', name: 'Arduino', icon: '🔌' },
    { id: 'books', name: 'Books', icon: '📚' },
    { id: 'electronics', name: 'Electronics', icon: '💻' },
    { id: 'components', name: 'Components', icon: '🔧' },
];

export function Marketplace() {
    const { isConnected, accountAddress } = usePeraWallet();
    const [listings] = useState(mockListings);
    const [activeCategory, setActiveCategory] = useState('all');
    const [showCreateModal, setShowCreateModal] = useState(false);

    const filteredListings = activeCategory === 'all'
        ? listings
        : listings.filter(l => l.category === activeCategory);

    const handleBuy = async (listing) => {
        if (!isConnected) {
            alert('Please connect your wallet to purchase');
            return;
        }

        // TODO: Integrate with P2P Listing contract
        alert(`Purchase initiated for ${listing.title} (${listing.price_algo} ALGO)`);
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                        🛒 P2P Marketplace
                    </h2>
                    <p className="text-slate-400 mt-1">Buy and sell Arduino kits, books, and more</p>
                </div>

                <button
                    onClick={() => setShowCreateModal(true)}
                    className="btn-primary"
                >
                    + List Item
                </button>
            </div>

            {/* Categories */}
            <div className="flex gap-2 overflow-x-auto pb-2">
                {categories.map(cat => (
                    <button
                        key={cat.id}
                        onClick={() => setActiveCategory(cat.id)}
                        className={`
              flex items-center gap-2 px-4 py-2 rounded-xl whitespace-nowrap transition-all
              ${activeCategory === cat.id
                                ? 'bg-emerald-500 text-white'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                            }
            `}
                    >
                        <span>{cat.icon}</span>
                        <span>{cat.name}</span>
                    </button>
                ))}
            </div>

            {/* Listings Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredListings.map((listing, index) => (
                    <div
                        key={listing.id}
                        className="glass-card p-5 animate-fade-in"
                        style={{ animationDelay: `${index * 100}ms` }}
                    >
                        {/* Image placeholder */}
                        <div className="bg-slate-800 rounded-xl h-40 flex items-center justify-center text-4xl mb-4">
                            {listing.category === 'arduino' && '🔌'}
                            {listing.category === 'books' && '📚'}
                            {listing.category === 'electronics' && '💻'}
                            {listing.category === 'components' && '🔧'}
                        </div>

                        {/* Content */}
                        <h3 className="text-lg font-semibold text-white mb-2">{listing.title}</h3>
                        <p className="text-slate-400 text-sm line-clamp-2 mb-3">{listing.description}</p>

                        {/* Condition badge */}
                        <span className={`
              inline-block px-2 py-1 text-xs rounded-full mb-3
              ${listing.condition === 'like_new'
                                ? 'bg-emerald-500/20 text-emerald-400'
                                : 'bg-amber-500/20 text-amber-400'
                            }
            `}>
                            {listing.condition === 'like_new' ? '✨ Like New' : '👍 Good'}
                        </span>

                        {/* Price and Buy */}
                        <div className="flex items-center justify-between pt-3 border-t border-slate-700">
                            <div>
                                <p className="text-2xl font-bold text-emerald-400">{listing.price_algo} ALGO</p>
                                <p className="text-xs text-slate-500">Seller: {listing.seller_address}</p>
                            </div>
                            <button
                                onClick={() => handleBuy(listing)}
                                className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl transition-colors"
                            >
                                Buy Now
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {filteredListings.length === 0 && (
                <div className="text-center py-12">
                    <span className="text-4xl">📭</span>
                    <p className="text-slate-400 mt-4">No items in this category</p>
                </div>
            )}
        </div>
    );
}

export default Marketplace;
