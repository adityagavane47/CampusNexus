/**
 * CampusNexus - Project Feed (Connected to Backend)
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { projectsService } from '../../services/projects';
import { CreateProjectModal } from './CreateProjectModal';

export function ProjectFeed() {
    const { user } = useAuth();
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
            await projectsService.createProject({
                ...projectData,
                creator_id: user.id
            });
            setIsModalOpen(false);
            loadProjects(); // Refresh the list
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
                {user && (
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="btn-primary"
                        style={{ padding: '8px 16px', fontSize: '0.875rem' }}
                    >
                        + Create Project
                    </button>
                )}
            </div>

            {/* Filter */}
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

                                {/* Creator Info */}
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
                                <button
                                    className="btn-primary"
                                    style={{ width: '100%' }}
                                    onClick={() => handleApply(project.id)}
                                    disabled={user?.id === project.creator_id}
                                >
                                    {user?.id === project.creator_id ? 'Your Project' : 'Apply Now'}
                                </button>
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
