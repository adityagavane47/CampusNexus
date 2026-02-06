/**
 * CampusNexus - Skill Matcher Component
 * AI-powered project matching for Track 2
 */
import { useState } from 'react';
import { matchProjects } from '../../services/ai';

export function SkillMatcher() {
    const [skillsInput, setSkillsInput] = useState('');
    const [matches, setMatches] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleMatch = async (e) => {
        e.preventDefault();
        if (!skillsInput.trim()) return;

        setIsLoading(true);
        try {
            const skillsList = skillsInput.split(',').map(s => s.trim());
            // In a real app we'd call the API:
            // const results = await matchProjects(skillsList);

            // For demo, we'll simulate the AI response since backend isn't connected to a real DB yet
            // This mimics the exact response structure of our FastAPI endpoint
            await new Promise(r => setTimeout(r, 1500)); // Simulate AI processing time

            const mockResults = [
                {
                    project_id: 1,
                    title: "Build IoT Dashboard",
                    match_score: 95.5,
                    skills_required: ["React", "Python", "IoT"]
                },
                {
                    project_id: 2,
                    title: "Smart Contract Audit",
                    match_score: 45.0,
                    skills_required: ["Solidity", "Security"]
                }
            ].filter(p => {
                // Simple client-side simulation of the Jaccard logic for the demo
                const pSkills = p.skills_required.map(s => s.toLowerCase());
                const uSkills = skillsList.map(s => s.toLowerCase());
                return pSkills.some(s => uSkills.includes(s));
            });

            // If no match in mock, return a generic one for demo purposes if relevant
            if (mockResults.length === 0 && skillsInput.toLowerCase().includes('react')) {
                mockResults.push({
                    project_id: 1,
                    title: "Build IoT Dashboard",
                    match_score: 80.0,
                    skills_required: ["React", "Python"]
                });
            }

            setMatches(mockResults);
        } catch (error) {
            console.error('Matching failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div className="section-header" style={{ textAlign: 'center', display: 'block' }}>
                <h2 className="section-title" style={{ fontSize: '2rem', marginBottom: '16px' }}>
                    ✨ AI Skill Matcher
                </h2>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Enter your skills and let our AI find the perfect projects for you.
                </p>
            </div>

            <div className="card" style={{ marginBottom: '40px' }}>
                <form onSubmit={handleMatch}>
                    <div style={{ marginBottom: '24px' }}>
                        <label style={{ fontSize: '0.875rem', marginBottom: '8px' }}>Your Skills (comma separated)</label>
                        <input
                            type="text"
                            placeholder="e.g. React, Python, Solidity, Figma"
                            value={skillsInput}
                            onChange={(e) => setSkillsInput(e.target.value)}
                            style={{
                                fontSize: '1.25rem',
                                padding: '16px',
                                width: '100%',
                                border: '1px solid var(--border-medium)'
                            }}
                        />
                    </div>
                    <button
                        type="submit"
                        className="btn-primary"
                        style={{ width: '100%', padding: '16px', fontSize: '1rem' }}
                        disabled={isLoading}
                    >
                        {isLoading ? '🤖 Analyzing Profile...' : 'Find Matches'}
                    </button>
                </form>
            </div>

            {matches && (
                <div className="animate-fade-in">
                    <h3 style={{ marginBottom: '24px' }}>Matches Found ({matches.length})</h3>

                    <div className="grid-2">
                        {matches.map(project => (
                            <div key={project.project_id} className="card" style={{ border: '1px solid var(--accent-black)' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                                    <div className="tag tag-dark">
                                        {project.match_score}% Match
                                    </div>
                                </div>

                                <h4 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>{project.title}</h4>

                                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '24px' }}>
                                    {project.skills_required.map(skill => (
                                        <span key={skill} className="tag">{skill}</span>
                                    ))}
                                </div>

                                <button className="btn-secondary" style={{ width: '100%' }}>
                                    View Project
                                </button>
                            </div>
                        ))}
                    </div>

                    {matches.length === 0 && (
                        <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                            <p>No matches found. Try adding more skills!</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default SkillMatcher;
