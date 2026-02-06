/**
 * CampusNexus - Create Project Modal (Minimalist Design)
 */
import { useState } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

export function CreateProjectModal({ isOpen, onClose, onSubmit }) {
    const { isConnected } = usePeraWallet();
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        budget: '',
        deadline: ''
    });

    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100,
            backdropFilter: 'blur(4px)'
        }}>
            <div
                className="animate-fade-in"
                style={{
                    backgroundColor: 'white',
                    borderRadius: '8px',
                    width: '100%',
                    maxWidth: '500px',
                    padding: '32px',
                    boxShadow: 'var(--shadow-lg)'
                }}
            >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
                    <h2 style={{ margin: 0 }}>Create Project</h2>
                    <button
                        onClick={onClose}
                        style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '1.5rem',
                            cursor: 'pointer',
                            color: 'var(--text-muted)'
                        }}
                    >
                        ×
                    </button>
                </div>

                <form onSubmit={(e) => { e.preventDefault(); onSubmit(formData); }}>
                    <div style={{ marginBottom: '16px' }}>
                        <label>Project Title</label>
                        <input
                            type="text"
                            placeholder="e.g. Redesign Landing Page"
                            value={formData.title}
                            onChange={e => setFormData({ ...formData, title: e.target.value })}
                            required
                        />
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label>Description</label>
                        <textarea
                            rows={4}
                            placeholder="Describe the deliverables..."
                            value={formData.description}
                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                            required
                        />
                    </div>

                    <div className="grid-2" style={{ marginBottom: '24px' }}>
                        <div>
                            <label>Budget (ALGO)</label>
                            <input
                                type="number"
                                placeholder="500"
                                value={formData.budget}
                                onChange={e => setFormData({ ...formData, budget: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label>Deadline</label>
                            <input
                                type="date"
                                value={formData.deadline}
                                onChange={e => setFormData({ ...formData, deadline: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn-secondary"
                            style={{ flex: 1 }}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="btn-primary"
                            style={{ flex: 1 }}
                        >
                            Post Project
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default CreateProjectModal;
