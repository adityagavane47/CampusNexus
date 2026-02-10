/**
 * CampusNexus - Main App Component
 * Minimalist Design - Clean & Modern
 */
import { useState } from 'react';
import { WalletConnect } from './components/wallet/WalletConnect';
import { NotificationBell } from './components/layout/NotificationBell';
import { ProjectFeed } from './components/feed/ProjectFeed';
import { CreateProjectModal } from './components/feed/CreateProjectModal';
import { Marketplace } from './components/marketplace/Marketplace';
import { Profile } from './components/profile/Profile';
import { SkillMatcher } from './components/feed/SkillMatcher';
import { LoginPage } from './components/auth/LoginPage';
import { OnboardingPage } from './components/auth/OnboardingPage';
import { useAuth } from './hooks/useAuth';
import { getCurrentNetwork } from './services/algorand';
import './index.css';

function App() {
    const [activeTab, setActiveTab] = useState('feed');
    const [showCreateModal, setShowCreateModal] = useState(false);
    const { user, loading, isAuthenticated, logout } = useAuth();

    // Check if user wants to skip login and use wallet directly
    const urlParams = new URLSearchParams(window.location.search);
    const skipLogin = urlParams.get('skip_login') === 'true';

    // Show login page if not authenticated and not skipping
    if (!isAuthenticated && !skipLogin && !loading) {
        return <LoginPage />;
    }

    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: 'var(--bg-primary)'
            }}>
                <p style={{ color: 'var(--text-muted)' }}>Loading...</p>
            </div>
        );
    }

    // Check if user needs to complete profile
    const isProfileComplete = user?.age && user?.year && user?.branch;

    if (isAuthenticated && !skipLogin && !isProfileComplete) {
        return <OnboardingPage onComplete={() => window.location.reload()} />;
    }

    const tabs = [
        { id: 'feed', label: 'Discover' },
        { id: 'matcher', label: '✨ AI Match' },
        { id: 'marketplace', label: 'Marketplace' },
        { id: 'profile', label: 'Profile' },
    ];

    const handleCreateProject = async (projectData) => {
        console.log('Creating project:', projectData);
        alert('Project created successfully!');
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-primary)' }}>
            {/* Navigation */}
            <nav style={{
                position: 'sticky',
                top: 0,
                zIndex: 50,
                backgroundColor: 'var(--bg-primary)',
                borderBottom: '1px solid var(--border-light)',
                padding: '0 24px',
            }}>
                <div style={{
                    maxWidth: '1200px',
                    margin: '0 auto',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    height: '72px',
                }}>
                    {/* Logo */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            backgroundColor: 'var(--accent-black)',
                            borderRadius: '8px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                        }}>
                            <span style={{ color: 'white', fontWeight: 700, fontSize: '1.125rem' }}>CN</span>
                        </div>
                        <div>
                            <h1 style={{ fontSize: '1.125rem', fontWeight: 600, margin: 0 }}>CampusNexus</h1>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>VIT Pune</p>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div style={{ display: 'flex', gap: '4px' }}>
                        {tabs.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                style={{
                                    padding: '10px 20px',
                                    fontSize: '0.875rem',
                                    fontWeight: 500,
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s',
                                    backgroundColor: activeTab === tab.id ? 'var(--bg-secondary)' : 'transparent',
                                    color: activeTab === tab.id ? 'var(--text-primary)' : 'var(--text-muted)',
                                }}
                            >
                                {tab.label}
                            </button>
                        ))}
                    </div>

                    {/* User Info / Wallet Connect */}
                    {isAuthenticated && user ? (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <NotificationBell />
                            <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                {user.email}
                            </span>
                            <button
                                onClick={logout}
                                style={{
                                    padding: '8px 16px',
                                    fontSize: '0.875rem',
                                    fontWeight: 500,
                                    border: '1px solid var(--border-light)',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    backgroundColor: 'transparent',
                                    color: 'var(--text-primary)',
                                    transition: 'all 0.2s'
                                }}
                            >
                                Logout
                            </button>
                        </div>
                    ) : (
                        <WalletConnect />
                    )}
                </div>
            </nav>

            {/* Hero Section */}
            <section style={{
                padding: '80px 24px',
                textAlign: 'center',
                backgroundColor: 'var(--bg-secondary)',
                borderBottom: '1px solid var(--border-light)',
            }}>
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                    <h2 style={{
                        fontSize: '2.5rem',
                        fontWeight: 600,
                        marginBottom: '16px',
                        letterSpacing: '-0.03em',
                    }}>
                        {activeTab === 'matcher' ? 'AI Skill Matching' : 'Discover Projects'}
                    </h2>
                    <p style={{
                        fontSize: '1rem',
                        color: 'var(--text-secondary)',
                        marginBottom: '32px',
                        lineHeight: 1.7,
                    }}>
                        {activeTab === 'matcher'
                            ? 'Our AI analyzes your skills to find the perfect freelance opportunities for you.'
                            : 'Find freelance opportunities, trade equipment, and build your on-chain reputation at VIT Pune.'
                        }
                    </p>

                    {activeTab === 'feed' && (
                        <button
                            onClick={() => setShowCreateModal(true)}
                            className="btn-primary"
                        >
                            Post a Project
                        </button>
                    )}
                </div>
            </section>

            {/* Stats */}
            <section style={{
                display: 'flex',
                justifyContent: 'center',
                gap: '64px',
                padding: '40px 24px',
                borderBottom: '1px solid var(--border-light)',
            }}>
                <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '1.5rem', fontWeight: 600, margin: 0 }}>150+</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Projects</p>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '1.5rem', fontWeight: 600, margin: 0 }}>500+</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Students</p>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '1.5rem', fontWeight: 600, margin: 0 }}>25K</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>ALGO Traded</p>
                </div>
            </section>

            {/* Main Content */}
            <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '48px 24px' }}>
                {activeTab === 'feed' && <ProjectFeed />}
                {activeTab === 'matcher' && <SkillMatcher />}
                {activeTab === 'marketplace' && <Marketplace />}
                {activeTab === 'profile' && <Profile />}
            </main>

            {/* Footer */}
            <footer style={{
                borderTop: '1px solid var(--border-light)',
                padding: '24px',
                textAlign: 'center',
            }}>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                    CampusNexus @ MADE BY TEAM AMATEUR
                </p>
            </footer>

            {/* Create Project Modal */}
            <CreateProjectModal
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onSubmit={handleCreateProject}
            />
        </div>
    );
}

export default App;
