/**
 * CampusNexus - Create Project Modal (Enhanced)
 */
import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';

export function CreateProjectModal({ isOpen, onClose, onSubmit }) {
    const { user } = useAuth();
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        budget_algo: '',
        deadline: '',
        skills_required: [],
        milestones: []
    });
    const [currentSkill, setCurrentSkill] = useState('');
    const [currentMilestone, setCurrentMilestone] = useState('');

    if (!isOpen) return null;

    const handleAddSkill = () => {
        if (currentSkill.trim() && !formData.skills_required.includes(currentSkill.trim())) {
            setFormData(prev => ({
                ...prev,
                skills_required: [...prev.skills_required, currentSkill.trim()]
            }));
            setCurrentSkill('');
        }
    };

    const handleRemoveSkill = (skillToRemove) => {
        setFormData(prev => ({
            ...prev,
            skills_required: prev.skills_required.filter(skill => skill !== skillToRemove)
        }));
    };

    const handleAddMilestone = () => {
        if (currentMilestone.trim()) {
            setFormData(prev => ({
                ...prev,
                milestones: [...prev.milestones, currentMilestone.trim()]
            }));
            setCurrentMilestone('');
        }
    };

    const handleRemoveMilestone = (index) => {
        setFormData(prev => ({
            ...prev,
            milestones: prev.milestones.filter((_, i) => i !== index)
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.skills_required.length === 0) {
            alert('Please add at least one required skill');
            return;
        }
        onSubmit(formData);
        // Reset form
        setFormData({
            title: '',
            description: '',
            budget_algo: '',
            deadline: '',
            skills_required: [],
            milestones: []
        });
    };

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
                    maxWidth: '600px',
                    maxHeight: '90vh',
                    overflow: 'auto',
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

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '16px' }}>
                        <label>Project Title *</label>
                        <input
                            type="text"
                            placeholder="e.g. Redesign Landing Page"
                            value={formData.title}
                            onChange={e => setFormData({ ...formData, title: e.target.value })}
                            required
                        />
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label>Description *</label>
                        <textarea
                            rows={4}
                            placeholder="Describe the deliverables..."
                            value={formData.description}
                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                            required
                        />
                    </div>

                    {/* Skills Input */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Required Skills *</label>
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                            <input
                                type="text"
                                value={currentSkill}
                                onChange={(e) => setCurrentSkill(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
                                placeholder="e.g., React, Python, Design"
                            />
                            <button
                                type="button"
                                onClick={handleAddSkill}
                                style={{
                                    padding: '8px 16px',
                                    borderRadius: '8px',
                                    backgroundColor: 'var(--bg-secondary)',
                                    border: '1px solid var(--border-light)',
                                    cursor: 'pointer',
                                    fontWeight: 500
                                }}
                            >
                                Add
                            </button>
                        </div>
                        {formData.skills_required.length > 0 && (
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                                {formData.skills_required.map((skill, index) => (
                                    <span
                                        key={index}
                                        style={{
                                            padding: '6px 12px',
                                            backgroundColor: 'black',
                                            color: 'white',
                                            borderRadius: '20px',
                                            fontSize: '0.875rem',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '6px'
                                        }}
                                    >
                                        {skill}
                                        <button
                                            type="button"
                                            onClick={() => handleRemoveSkill(skill)}
                                            style={{
                                                background: 'none',
                                                border: 'none',
                                                color: 'white',
                                                cursor: 'pointer',
                                                padding: '0',
                                                fontSize: '1.2rem',
                                                lineHeight: 1
                                            }}
                                        >
                                            ×
                                        </button>
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Milestones */}
                    <div style={{ marginBottom: '16px' }}>
                        <label>Milestones (optional)</label>
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                            <input
                                type="text"
                                value={currentMilestone}
                                onChange={(e) => setCurrentMilestone(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddMilestone())}
                                placeholder="e.g., Initial design mockup"
                            />
                            <button
                                type="button"
                                onClick={handleAddMilestone}
                                style={{
                                    padding: '8px 16px',
                                    borderRadius: '8px',
                                    backgroundColor: 'var(--bg-secondary)',
                                    border: '1px solid var(--border-light)',
                                    cursor: 'pointer',
                                    fontWeight: 500
                                }}
                            >
                                Add
                            </button>
                        </div>
                        {formData.milestones.length > 0 && (
                            <ul style={{ paddingLeft: '20px', fontSize: '0.875rem' }}>
                                {formData.milestones.map((milestone, index) => (
                                    <li key={index} style={{ marginBottom: '4px', display: 'flex', justifyContent: 'space-between' }}>
                                        <span>{milestone}</span>
                                        <button
                                            type="button"
                                            onClick={() => handleRemoveMilestone(index)}
                                            style={{
                                                background: 'none',
                                                border: 'none',
                                                cursor: 'pointer',
                                                color: 'var(--text-error)',
                                                padding: '0'
                                            }}
                                        >
                                            ×
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>

                    <div className="grid-2" style={{ marginBottom: '24px' }}>
                        <div>
                            <label>Budget (ALGO) *</label>
                            <input
                                type="number"
                                step="0.01"
                                placeholder="500"
                                value={formData.budget_algo}
                                onChange={e => setFormData({ ...formData, budget_algo: parseFloat(e.target.value) })}
                                required
                            />
                        </div>
                        <div>
                            <label>Deadline *</label>
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
