/**
 * CampusNexus - Create Project Modal
 * Form for creating new projects with escrow
 */
import { useState } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';

export function CreateProjectModal({ isOpen, onClose, onSubmit }) {
    const { isConnected, accountAddress } = usePeraWallet();
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        skills: '',
        budget: '',
        deadline: '',
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    if (!isOpen) return null;

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!isConnected) {
            alert('Please connect your wallet first');
            return;
        }

        setIsSubmitting(true);

        try {
            await onSubmit({
                ...formData,
                skills_required: formData.skills.split(',').map(s => s.trim()),
                budget_algo: parseFloat(formData.budget),
                creator_address: accountAddress,
            });
            onClose();
            setFormData({ title: '', description: '', skills: '', budget: '', deadline: '' });
        } catch (error) {
            console.error('Submit error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="relative bg-slate-900 border border-slate-700 rounded-2xl p-6 w-full max-w-lg mx-4 animate-fade-in">
                <h2 className="text-2xl font-bold text-white mb-6">
                    🚀 Create New Project
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Title */}
                    <div>
                        <label className="block text-sm text-slate-400 mb-1">Project Title</label>
                        <input
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            required
                            placeholder="e.g., Build IoT Dashboard"
                            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                        />
                    </div>

                    {/* Description */}
                    <div>
                        <label className="block text-sm text-slate-400 mb-1">Description</label>
                        <textarea
                            name="description"
                            value={formData.description}
                            onChange={handleChange}
                            required
                            rows={3}
                            placeholder="Describe what you need..."
                            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none"
                        />
                    </div>

                    {/* Skills */}
                    <div>
                        <label className="block text-sm text-slate-400 mb-1">Required Skills (comma-separated)</label>
                        <input
                            type="text"
                            name="skills"
                            value={formData.skills}
                            onChange={handleChange}
                            required
                            placeholder="e.g., React, Python, Arduino"
                            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                        />
                    </div>

                    {/* Budget and Deadline */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm text-slate-400 mb-1">Budget (ALGO)</label>
                            <input
                                type="number"
                                name="budget"
                                value={formData.budget}
                                onChange={handleChange}
                                required
                                min="1"
                                step="0.1"
                                placeholder="50"
                                className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-slate-400 mb-1">Deadline</label>
                            <input
                                type="date"
                                name="deadline"
                                value={formData.deadline}
                                onChange={handleChange}
                                required
                                className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                            />
                        </div>
                    </div>

                    {/* Wallet warning */}
                    {!isConnected && (
                        <div className="bg-amber-500/20 border border-amber-500/50 rounded-xl p-3 text-amber-400 text-sm">
                            ⚠️ Connect your wallet to create a project with escrow
                        </div>
                    )}

                    {/* Actions */}
                    <div className="flex gap-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-xl transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isSubmitting || !isConnected}
                            className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isSubmitting ? 'Creating...' : 'Create Project'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default CreateProjectModal;
