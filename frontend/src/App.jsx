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
import './index.css';

function App() {
    const [activeTab, setActiveTab] = useState('feed');
    const [showCreateModal, setShowCreateModal] = useState(false);
    const { user, loading, isAuthenticated, logout } = useAuth();

    const urlParams = new URLSearchParams(window.location.search);
    const skipLogin = urlParams.get('skip_login') === 'true';

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
                backgroundColor: 'var(--bg-primary)',
                flexDirection: 'column',
                gap: '16px',
            }}>
                <div style={{
                    width: '48px',
                    height: '48px',
                    border: '2px solid var(--border-subtle)',
                    borderTopColor: 'var(--accent-teal)',
                    borderRadius: '50%',
                    animation: 'rotate 0.8s linear infinite',
                }} />
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Loading...</p>
            </div>
        );
    }

    const isProfileComplete = user?.age && user?.year && user?.branch;
    if (isAuthenticated && !skipLogin && !isProfileComplete) {
        return <OnboardingPage onComplete={() => window.location.reload()} />;
    }

    const tabs = [
        { id: 'feed', label: 'Discover', icon: '⚡' },
        { id: 'matcher', label: 'AI Match', icon: '🤖' },
        { id: 'marketplace', label: 'Marketplace', icon: '🛒' },
        { id: 'profile', label: 'Profile', icon: '👤' },
    ];

    const heroCopy = {
        feed: {
            badge: 'LIVE OPPORTUNITIES',
            title: 'Build. Collaborate.\nGet Paid On-Chain.',
            sub: 'Find freelance projects, apply with your skills, and get paid securely via Algorand smart contracts.',
        },
        matcher: {
            badge: 'AI POWERED',
            title: 'Your Skills.\nPerfect Match.',
            sub: 'Our AI engine analyzes your skill profile and surfaces the most relevant opportunities for you.',
        },
    };

    const hero = heroCopy[activeTab];

    return (
        <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-primary)', position: 'relative' }}>

            
            <div style={{
                position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                pointerEvents: 'none', zIndex: 0, overflow: 'hidden',
            }}>
                <div style={{
                    position: 'absolute', top: '-15%', left: '30%',
                    width: '600px', height: '600px',
                    background: 'radial-gradient(circle, rgba(0,212,170,0.06) 0%, transparent 70%)',
                }} />
                <div style={{
                    position: 'absolute', bottom: '-10%', right: '10%',
                    width: '400px', height: '400px',
                    background: 'radial-gradient(circle, rgba(0,188,212,0.04) 0%, transparent 70%)',
                }} />
            </div>

            
            <nav style={{
                position: 'sticky', top: 0, zIndex: 50,
                backgroundColor: 'rgba(6, 11, 16, 0.85)',
                borderBottom: '1px solid var(--border-subtle)',
                padding: '0 24px',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
            }}>
                <div style={{
                    maxWidth: '1200px', margin: '0 auto',
                    display: 'flex', alignItems: 'center',
                    justifyContent: 'space-between', height: '68px',
                }}>
                    
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{
                            width: '38px', height: '38px',
                            background: 'linear-gradient(135deg, rgba(0,212,170,0.25), rgba(0,188,212,0.15))',
                            border: '1px solid rgba(0,212,170,0.35)',
                            borderRadius: '10px',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            boxShadow: '0 0 16px rgba(0,212,170,0.2)',
                        }}>
                            <span style={{ color: 'var(--accent-teal)', fontWeight: 800, fontSize: '1rem' }}>CN</span>
                        </div>
                        <span style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
                            CampusNexus
                        </span>
                    </div>

                    
                    <div style={{
                        display: 'flex', gap: '2px',
                        background: 'var(--bg-glass)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '12px', padding: '4px',
                    }}>
                        {tabs.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                style={{
                                    padding: '8px 18px',
                                    fontSize: '0.8375rem',
                                    fontWeight: 500,
                                    border: 'none',
                                    borderRadius: '8px',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s ease',
                                    display: 'flex', alignItems: 'center', gap: '6px',
                                    background: activeTab === tab.id
                                        ? 'linear-gradient(135deg, rgba(0,212,170,0.2), rgba(0,188,212,0.12))'
                                        : 'transparent',
                                    color: activeTab === tab.id ? 'var(--accent-teal)' : 'var(--text-muted)',
                                    boxShadow: activeTab === tab.id ? '0 0 12px rgba(0,212,170,0.15)' : 'none',
                                }}
                            >
                                <span style={{ fontSize: '0.85em' }}>{tab.icon}</span>
                                {tab.label}
                            </button>
                        ))}
                    </div>

                    
                    {isAuthenticated && user ? (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <NotificationBell />
                            <div style={{
                                display: 'flex', alignItems: 'center', gap: '8px',
                                padding: '6px 12px',
                                background: 'var(--bg-glass)',
                                border: '1px solid var(--border-subtle)',
                                borderRadius: '10px',
                            }}>
                                <div style={{
                                    width: '28px', height: '28px',
                                    borderRadius: '50%',
                                    background: 'linear-gradient(135deg, var(--accent-teal), var(--accent-cyan))',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    fontSize: '0.75rem', fontWeight: 700, color: '#060b10',
                                }}>
                                    {user.email?.[0]?.toUpperCase() || 'U'}
                                </div>
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', maxWidth: '140px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                    {user.email}
                                </span>
                            </div>
                            <button
                                onClick={logout}
                                className="btn-ghost"
                                style={{ fontSize: '0.8125rem' }}
                            >
                                Logout
                            </button>
                        </div>
                    ) : (
                        <WalletConnect />
                    )}
                </div>
            </nav>

            
            {hero && (
                <section style={{
                    padding: '80px 24px 64px',
                    textAlign: 'center',
                    position: 'relative',
                    zIndex: 1,
                }}>
                    
                    <div style={{
                        position: 'absolute', inset: 0,
                        backgroundImage: 'linear-gradient(rgba(0,212,170,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,170,0.025) 1px, transparent 1px)',
                        backgroundSize: '60px 60px',
                        maskImage: 'radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 100%)',
                        WebkitMaskImage: 'radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 100%)',
                        pointerEvents: 'none',
                    }} />

                    <div style={{ maxWidth: '700px', margin: '0 auto', position: 'relative' }}>
                        
                        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '24px' }}>
                            <div style={{
                                padding: '4px 14px', background: 'var(--accent-teal-dim)',
                                border: '1px solid rgba(0,212,170,0.3)', borderRadius: '100px',
                                fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.08em',
                                color: 'var(--accent-teal)',
                            }}>
                                ● {hero.badge}
                            </div>
                        </div>

                        <h1 style={{
                            fontSize: '3.25rem', fontWeight: 800, marginBottom: '20px',
                            letterSpacing: '-0.04em', lineHeight: 1.1,
                            background: 'linear-gradient(135deg, #ffffff 0%, #a8d8e8 60%, var(--accent-teal) 100%)',
                            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
                            whiteSpace: 'pre-line',
                        }}>
                            {hero.title}
                        </h1>

                        <p style={{
                            fontSize: '1.0625rem', color: 'var(--text-secondary)',
                            marginBottom: '36px', lineHeight: 1.75, maxWidth: '520px', margin: '0 auto 36px',
                        }}>
                            {hero.sub}
                        </p>

                        {activeTab === 'feed' && (
                            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
                                <button
                                    onClick={() => setShowCreateModal(true)}
                                    className="btn-primary"
                                    style={{ padding: '14px 32px', fontSize: '0.9375rem' }}
                                >
                                    + Post a Project
                                </button>
                                <button className="btn-secondary" style={{ padding: '14px 28px', fontSize: '0.9375rem' }}>
                                    Browse All →
                                </button>
                            </div>
                        )}

                    </div>
                </section>
            )}

            
            <main style={{
                maxWidth: '1200px', margin: '0 auto',
                padding: hero ? '0 24px 80px' : '48px 24px 80px',
                position: 'relative', zIndex: 1,
            }}>
                {activeTab === 'feed' && <ProjectFeed />}
                {activeTab === 'matcher' && <SkillMatcher />}
                {activeTab === 'marketplace' && <Marketplace />}
                {activeTab === 'profile' && <Profile />}
            </main>

            
            <footer style={{
                borderTop: '1px solid var(--border-subtle)',
                padding: '24px',
                textAlign: 'center',
                position: 'relative', zIndex: 1,
            }}>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                    CampusNexus &nbsp;·&nbsp; Built by Team Amateur &nbsp;·&nbsp;
                    <span style={{ color: 'var(--accent-teal)' }}>Powered by Algorand</span>
                </p>
            </footer>

            
            <CreateProjectModal
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onSubmit={async (data) => {
                    console.log('Creating project:', data);
                    alert('Project created successfully!');
                }}
            />
        </div>
    );
}

export default App;
