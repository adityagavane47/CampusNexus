/**
 * CampusNexus - Project Feed (Connected to Backend)
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useEscrow } from '../../hooks/useEscrow';
import { usePeraWallet } from '../../hooks/usePeraWallet';
import { projectsService } from '../../services/projects';
import { CreateProjectModal } from './CreateProjectModal';

export function ProjectFeed() {
    const { user } = useAuth();
    const { accountAddress, connect: connectWallet, isConnected, signTransaction } = usePeraWallet();
    const { createEscrow, isLoading: escrowLoading, error: escrowError } = useEscrow();
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [skillFilter, setSkillFilter] = useState('');

    useEffect(() => {
        loadProjects();
    }, [skillFilter]);

    const loadProjects = async () => {
        try {
            setLoading(true);
            setError(null);
            const filters = skillFilter ? { skill: skillFilter } : {};
            const data = await projectsService.getProjects(filters);
            setProjects(data);
        } catch (err) {
            setError('Failed to load projects');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateProject = async (projectData) => {
        try {
            let escrowData = {};

            // If escrow is enabled, verify wallet and store intent
            if (projectData.enableEscrow) {
                let walletAddress = accountAddress;

                if (!isConnected || !accountAddress) {
                    alert('Please connect your Algorand wallet to enable escrow protection.');
                    const connectedAddress = await connectWallet();

                    if (!connectedAddress) {
                        alert('Wallet connection cancelled. Project not created.');
                        return;
                    }

                    walletAddress = connectedAddress;
                }

                // Store escrow intent - actual smart contract will be created
                // when a freelancer applicant is accepted (needs their address)
                escrowData = {
                    escrow_enabled: true,
                    client_wallet: walletAddress,
                    budget_algo: projectData.budget_algo,
                    num_milestones: projectData.milestones.length || 1,
                };

                console.log('Escrow protection enabled with wallet:', walletAddress);
            }

            // Submit project to backend
            await projectsService.createProject({
                ...projectData,
                creator_id: user.id,
                ...escrowData,
            });

            setIsModalOpen(false);
            loadProjects();

            if (escrowData.escrow_enabled) {
                alert('Project created with escrow protection enabled! The smart contract will be deployed when you accept a freelancer.');
            }
        } catch (err) {
            alert('Failed to create project. Please try again.');
            console.error(err);
        }
    };

    const handleApply = async (projectId) => {
        if (!user) {
            alert('Please log in to apply to projects');
            return;
        }

        try {
            await projectsService.applyToProject(projectId, user.id);
            alert('Application submitted successfully!');
            loadProjects(); // Refresh to show updated application count
        } catch (err) {
            alert('Failed to apply. You may have already applied.');
            console.error(err);
        }
    };

    if (loading) {
        return <div className="animate-fade-in" style={{ textAlign: 'center', padding: '48px' }}>Loading projects...</div>;
    }

    if (error) {
        return <div className="animate-fade-in" style={{ textAlign: 'center', padding: '48px', color: 'var(--text-error)' }}>{error}</div>;
    }

    return (
        <div className="animate-fade-in">
            <div className="section-header">
                <h2 className="section-title">Latest Opportunities</h2>
                <button
                    onClick={() => {
                        if (!user) {
                            alert('Please log in to create a project');
                            return;
                        }
                        setIsModalOpen(true);
                    }}
                    className="btn-primary"
                    style={{ padding: '8px 16px', fontSize: '0.875rem' }}
                >
                    + Create Project
                </button>
            </div>

            <div style={{ marginBottom: '24px' }}>
                <input
                    type="text"
                    placeholder="Filter by skill (e.g., React, Python)..."
                    value={skillFilter}
                    onChange={(e) => setSkillFilter(e.target.value)}
                    style={{
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid var(--border-light)',
                        width: '100%',
                        maxWidth: '400px'
                    }}
                />
            </div>

            {projects.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '48px' }}>
                    <p style={{ color: 'var(--text-muted)' }}>No projects found. {user ? 'Be the first to create one!' : 'Log in to create projects.'}</p>
                </div>
            ) : (
                <div className="grid-3">
                    {projects.map(project => (
                        <div key={project.id} className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                            <div style={{ marginBottom: '16px' }}>
                                {project.skills_required && project.skills_required.length > 0 && (
                                    <span className="tag" style={{ marginBottom: '12px' }}>{project.skills_required[0]}</span>
                                )}
                                <h3 style={{ fontSize: '1.25rem', marginBottom: '8px' }}>{project.title}</h3>
                                <p style={{ fontSize: '0.875rem', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
                                    {project.description}
                                </p>

                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '12px' }}>
                                    <div style={{
                                        width: '24px',
                                        height: '24px',
                                        borderRadius: '50%',
                                        backgroundColor: 'var(--bg-secondary)',
                                        overflow: 'hidden',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center'
                                    }}>
                                        {project.creator_avatar ? (
                                            <img src={project.creator_avatar} alt={project.creator_name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                                        ) : (
                                            <span style={{ fontSize: '0.75rem' }}>👤</span>
                                        )}
                                    </div>
                                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                        by {project.creator_name}
                                    </span>
                                </div>
                            </div>

                            <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--border-light)' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                                    <div>
                                        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Budget</p>
                                        <p style={{ fontWeight: 600 }}>{project.budget_algo} ALGO</p>
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Applications</p>
                                        <p style={{ fontWeight: 500 }}>{project.applications?.length || 0}</p>
                                    </div>
                                </div>

                                {/* Show different views for creator vs applicant */}
                                {user?.id === project.creator_id ? (
                                    /* Creator View: Show Applicants */
                                    <div>
                                        {project.applications && project.applications.length > 0 ? (
                                            <div>
                                                <p style={{ fontSize: '0.875rem', fontWeight: 600, marginBottom: '12px' }}>
                                                    Applicants ({project.applications.length})
                                                </p>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                                                    {project.applications.map((applicant, idx) => (
                                                        <div key={idx} style={{
                                                            display: 'flex',
                                                            justifyContent: 'space-between',
                                                            alignItems: 'center',
                                                            padding: '8px',
                                                            backgroundColor: 'var(--bg-secondary)',
                                                            borderRadius: '4px'
                                                        }}>
                                                            <span style={{ fontSize: '0.875rem' }}>{applicant.user_name}</span>
                                                            {project.status === 'open' && (
                                                                <button
                                                                    className="btn-primary"
                                                                    style={{ padding: '4px 12px', fontSize: '0.75rem' }}
                                                                    onClick={async () => {
                                                                        if (!accountAddress) {
                                                                            alert('Please connect your wallet first');
                                                                            await connectWallet();
                                                                            return;
                                                                        }

                                                                        if (window.confirm(`Hire ${applicant.user_name}? This will deploy a Smart Contract and lock ${project.budget_algo} ALGO.`)) {
                                                                            try {
                                                                                // 1. Deploy & Fund Escrow Contract
                                                                                const escrowResult = await createEscrow(
                                                                                    accountAddress,
                                                                                    signTransaction,
                                                                                    applicant.user_wallet || accountAddress,
                                                                                    project.budget_algo,
                                                                                    project.milestones?.length || 1
                                                                                );

                                                                                if (!escrowResult || !escrowResult.applicationIndex) {
                                                                                    throw new Error('Failed to deploy escrow contract');
                                                                                }

                                                                                const escrowAppId = escrowResult.applicationIndex;

                                                                                console.log('Creating hire record with escrow ID:', escrowAppId);

                                                                                // Update backend with hire info
                                                                                const response = await fetch(`http://localhost:8000/api/feed/${project.id}/hire`, {
                                                                                    method: 'POST',
                                                                                    headers: { 'Content-Type': 'application/json' },
                                                                                    body: JSON.stringify({
                                                                                        freelancer_id: applicant.user_id,
                                                                                        freelancer_wallet: applicant.user_wallet || accountAddress,
                                                                                        escrow_app_id: escrowAppId
                                                                                    })
                                                                                });

                                                                                if (!response.ok) {
                                                                                    throw new Error('Failed to hire');
                                                                                }

                                                                                alert(`✅ Successfully hired ${applicant.user_name}!\n\nEscrow Contract Deployed: ${escrowAppId}\nFunds Locked: ${project.budget_algo} ALGO`);
                                                                                loadProjects(); // Refresh
                                                                            } catch (err) {
                                                                                console.error('Hire error:', err);
                                                                                alert('Failed to hire applicant: ' + err.message);
                                                                            }
                                                                        }
                                                                    }}
                                                                >
                                                                    Hire & Fund
                                                                </button>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        ) : (
                                            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', textAlign: 'center' }}>
                                                No applicants yet
                                            </p>
                                        )}
                                    </div>
                                ) : (
                                    /* Applicant View: Show Apply Button */
                                    <button
                                        className="btn-primary"
                                        style={{ width: '100%' }}
                                        onClick={() => handleApply(project.id)}
                                    >
                                        Apply Now
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {user && (
                <CreateProjectModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    onSubmit={handleCreateProject}
                />
            )}
        </div>
    );
}

export default ProjectFeed;
