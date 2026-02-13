/**
 * CampusNexus - Create Listing Modal
 * Upload image to IPFS and create blockchain listing
 */
import { useState } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

const API_BASE = 'http://localhost:8000/api';

export function CreateListingModal({ onClose, onSuccess }) {
    const { sendTransaction, accountAddress } = usePeraWallet();

    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: 'arduino',
        price_algo: '',
        condition: 'good',
        ipfs_cid: ''
    });

    const [imageFile, setImageFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    const handleImageChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setImageFile(file);
        setUploading(true);

        try {
            const formDataObj = new FormData();
            formDataObj.append('file', file);

            const response = await fetch(`${API_BASE}/marketplace/upload-image`, {
                method: 'POST',
                body: formDataObj
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            setFormData(prev => ({ ...prev, ipfs_cid: data.cid }));

            console.log('Image uploaded to IPFS:', data.gateway_url);
        } catch (error) {
            console.error('IPFS upload error:', error);
            alert('Failed to upload image. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!formData.ipfs_cid) {
            alert('Please upload an image first');
            return;
        }

        setSubmitting(true);

        try {
            // Create listing in backend (metadata storage)
            const response = await fetch(`${API_BASE}/marketplace/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...formData,
                    seller_address: accountAddress,
                    status: 'available'
                })
            });

            if (!response.ok) throw new Error('Failed to create listing');

            const listing = await response.json();

            // TODO: When smart contracts are deployed, add blockchain transaction:
            // const txn = await sendTransaction({
            //     type: 'appl',
            //     appIndex: MARKETPLACE_APP_ID,
            //     appArgs: [
            //         'create_listing',
            //         formData.title,
            //         formData.category,
            //         formData.price_algo * 1_000_000,
            //         formData.ipfs_cid
            //     ]
            // });

            onSuccess(listing);
            onClose();
        } catch (error) {
            console.error('Listing creation error:', error);
            alert('Failed to create listing. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
                <div className="modal-header">
                    <h2>Create Listing</h2>
                    <button onClick={onClose} className="btn-close">✕</button>
                </div>

                <form onSubmit={handleSubmit} style={{ padding: '24px' }}>
                    {/* Image Upload */}
                    <div style={{ marginBottom: '24px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
                            Item Image
                        </label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageChange}
                            disabled={uploading}
                            style={{ marginBottom: '8px' }}
                        />
                        {uploading && <p style={{ color: 'var(--accent-purple)' }}>📤 Uploading to IPFS...</p>}
                        {formData.ipfs_cid && <p style={{ color: 'var(--accent-green)' }}>✅ Image uploaded: {formData.ipfs_cid.substring(0, 12)}...</p>}
                    </div>

                    {/* Title */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Title</label>
                        <input
                            type="text"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                            required
                            placeholder="Arduino Uno R3 Kit"
                        />
                    </div>

                    {/* Description */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Description</label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            required
                            rows="3"
                            placeholder="Describe your item..."
                        />
                    </div>

                    {/* Category */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Category</label>
                        <select
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                        >
                            <option value="arduino">Arduino & Electronics</option>
                            <option value="books">Books & Notes</option>
                            <option value="laptops">Laptops & Computers</option>
                            <option value="components">Electronic Components</option>
                            <option value="lab_equipment">Lab Equipment</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    {/* Price */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Price (ALGO)</label>
                        <input
                            type="number"
                            step="0.1"
                            value={formData.price_algo}
                            onChange={(e) => setFormData({ ...formData, price_algo: e.target.value })}
                            required
                            placeholder="15.0"
                        />
                    </div>

                    {/* Condition */}
                    <div style={{ marginBottom: '24px' }}>
                        <label>Condition</label>
                        <select
                            value={formData.condition}
                            onChange={(e) => setFormData({ ...formData, condition: e.target.value })}
                        >
                            <option value="new">New</option>
                            <option value="like_new">Like New</option>
                            <option value="good">Good</option>
                            <option value="fair">Fair</option>
                        </select>
                    </div>

                    <button
                        type="submit"
                        className="btn-primary"
                        style={{ width: '100%', padding: '14px' }}
                        disabled={uploading || submitting}
                    >
                        {submitting ? '⏳ Creating Listing...' : '🚀 List Item'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default CreateListingModal;
