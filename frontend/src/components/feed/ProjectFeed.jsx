/**
 * CampusNexus - Project Feed (Minimalist Design)
 */
import { useState } from 'react';

const mockProjects = [
    {
        id: 1,
        title: "Build IoT Dashboard",
        budget: 500,
        deadline: "2024-03-20",
        skills: ["React", "Python"],
        description: "Need a dashboard to visualize sensor data from Arduino."
    },
    {
        id: 2,
        title: "Mobile App UI",
        budget: 300,
        deadline: "2024-03-15",
        skills: ["Figma", "UI/UX"],
        description: "Design a clean, minimalist mobile app interface for a startup."
    },
    {
        id: 3,
        title: "Smart Contract Audit",
        budget: 1000,
        deadline: "2024-04-01",
        skills: ["Solidity", "Security"],
        description: "Audit our new DeFi protocol smart contracts."
    }
];

export function ProjectFeed() {
    return (
        <div className="animate-fade-in">
            <div className="section-header">
                <h2 className="section-title">Latest Opportunities</h2>
                <a href="#" className="section-link">View All</a>
            </div>

            <div className="grid-3">
                {mockProjects.map(project => (
                    <div key={project.id} className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                        <div style={{ marginBottom: '16px' }}>
                            <span className="tag" style={{ marginBottom: '12px' }}>{project.skills[0]}</span>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '8px' }}>{project.title}</h3>
                            <p style={{ fontSize: '0.875rem', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
                                {project.description}
                            </p>
                        </div>

                        <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--border-light)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                                <div>
                                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Budget</p>
                                    <p style={{ fontWeight: 600 }}>{project.budget} ALGO</p>
                                </div>
                                <div style={{ textAlign: 'right' }}>
                                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Deadline</p>
                                    <p style={{ fontWeight: 500 }}>{project.deadline}</p>
                                </div>
                            </div>
                            <button className="btn-primary" style={{ width: '100%' }}>
                                Apply Now
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ProjectFeed;
