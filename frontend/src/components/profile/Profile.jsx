/**
 * CampusNexus - Profile Component (Minimalist Design)
 */
import { useState, useEffect } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';
import { useAuth } from '../../hooks/useAuth';
import { getAccountBalance } from '../../services/algorand';

export function Profile() {
    const { isConnected, accountAddress } = usePeraWallet();
    const { user } = useAuth();
    const [balance, setBalance] = useState(0);
    const [isEditingName, setIsEditingName] = useState(false);
    const [editedName, setEditedName] = useState('');
    const [isEditingBio, setIsEditingBio] = useState(false);
    const [editedBio, setEditedBio] = useState('');

    useEffect(() => {
        if (isConnected && accountAddress) {
            getAccountBalance(accountAddress).then(setBalance);
        }
    }, [isConnected, accountAddress]);

    const handleSaveName = async () => {
        if (!editedName.trim()) {
            alert('Name cannot be empty');
            return;
        }
        try {
            const { authService } = await import('../../services/auth');
            await authService.updateProfile(user.id, { name: editedName });
            setIsEditingName(false);
            window.location.reload(); // Refresh to show updated data
        } catch (error) {
            console.error('Failed to update name:', error);
            alert('Failed to update name');
        }
    };

    const handleSaveBio = async () => {
        try {
            const { authService } = await import('../../services/auth');
            await authService.updateProfile(user.id, { bio: editedBio });
            setIsEditingBio(false);
            window.location.reload(); // Refresh to show updated data
        } catch (error) {
            console.error('Failed to update bio:', error);
            alert('Failed to update bio');
        }
    };

    if (!isConnected && !user) {
        return (
            <div style={{
                minHeight: '400px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
            }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '16px' }}>Sign in to view profile</h2>
            </div>
        );
    }

    return (
        <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '24px',
                marginBottom: '48px',
                padding: '24px',
                backgroundColor: 'var(--bg-secondary)',
                borderRadius: '16px'
            }}>
                <div style={{
                    width: '80px',
                    height: '80px',
                    borderRadius: '50%',
                    backgroundColor: 'var(--accent-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '2rem',
                    color: 'white',
                    overflow: 'hidden'
                }}>
                    {user?.profile_picture ? (
                        <img
                            src={user.profile_picture}
                            alt="Profile"
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        />
                    ) : user?.avatar ? (
                        <img
                            src={user.avatar}
                            alt="Avatar"
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        />
                    ) : '👤'}
                </div>
                <div style={{ flex: 1 }}>
                    {isEditingName ? (
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '4px' }}>
                            <input
                                type="text"
                                value={editedName}
                                onChange={(e) => setEditedName(e.target.value)}
                                style={{
                                    fontSize: '1.5rem',
                                    padding: '4px 8px',
                                    borderRadius: '4px',
                                    border: '1px solid var(--border-light)',
                                    flex: 1
                                }}
                            />
                            <button onClick={handleSaveName} style={{ padding: '4px 12px', borderRadius: '4px', background: 'black', color: 'white', border: 'none', cursor: 'pointer' }}>Save</button>
                            <button onClick={() => setIsEditingName(false)} style={{ padding: '4px 12px', borderRadius: '4px', background: 'var(--bg-secondary)', border: '1px solid var(--border-light)', cursor: 'pointer' }}>Cancel</button>
                        </div>
                    ) : (
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                            <h2 style={{ fontSize: '1.5rem', margin: 0 }}>{user?.name || "Anonymous User"}</h2>
                            <button
                                onClick={() => { setEditedName(user?.name || ''); setIsEditingName(true); }}
                                style={{
                                    background: 'none',
                                    border: 'none',
                                    cursor: 'pointer',
                                    fontSize: '0.875rem',
                                    color: 'var(--text-secondary)',
                                    padding: '2px 8px',
                                    borderRadius: '4px',
                                    transition: 'background 0.2s'
                                }}
                                onMouseEnter={(e) => e.target.style.background = 'var(--bg-secondary)'}
                                onMouseLeave={(e) => e.target.style.background = 'none'}
                            >
                                ✏️ Edit
                            </button>
                        </div>
                    )}
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>
                        {user?.branch ? `${user.branch} • ${user.year}` : user?.college}
                    </p>
                    {accountAddress && (
                        <p style={{ fontFamily: 'monospace', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                            {accountAddress.slice(0, 6)}...{accountAddress.slice(-6)}
                        </p>
                    )}
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid-3" style={{ marginBottom: '48px' }}>
                <div className="card-minimal" style={{ backgroundColor: 'var(--bg-secondary)', textAlign: 'center' }}>
                    <p style={{ fontSize: '2rem', fontWeight: 600 }}>{balance.toFixed(1)}</p>
                    <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>ALGO Balance</p>
                </div>
                <div className="card-minimal" style={{ backgroundColor: 'var(--bg-secondary)', textAlign: 'center' }}>
                    <p style={{ fontSize: '2rem', fontWeight: 600 }}>100</p>
                    <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Hustle Score</p>
                </div>
                <div className="card-minimal" style={{ backgroundColor: 'var(--bg-secondary)', textAlign: 'center' }}>
                    <p style={{ fontSize: '2rem', fontWeight: 600 }}>5★</p>
                    <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Rating</p>
                </div>
            </div>

            {/* Skills Section */}
            {user?.skills && user.skills.length > 0 && (
                <div className="card" style={{ marginBottom: '48px' }}>
                    <div className="section-header">
                        <h3 className="section-title" style={{ fontSize: '1rem' }}>Skills</h3>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', padding: '8px 0' }}>
                        {user.skills.map((skill, index) => (
                            <span
                                key={index}
                                style={{
                                    padding: '6px 16px',
                                    backgroundColor: 'black',
                                    color: 'white',
                                    borderRadius: '20px',
                                    fontSize: '0.875rem',
                                    fontWeight: 500
                                }}
                            >
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* About Me Section */}
            <div className="card" style={{ marginBottom: '48px' }}>
                <div className="section-header">
                    <h3 className="section-title" style={{ fontSize: '1rem' }}>About Me</h3>
                    {!isEditingBio && (
                        <button
                            onClick={() => { setEditedBio(user?.bio || ''); setIsEditingBio(true); }}
                            style={{
                                background: 'none',
                                border: 'none',
                                cursor: 'pointer',
                                fontSize: '0.875rem',
                                color: 'var(--text-secondary)',
                                padding: '4px 12px',
                                borderRadius: '4px',
                                transition: 'background 0.2s'
                            }}
                            onMouseEnter={(e) => e.target.style.background = 'var(--bg-secondary)'}
                            onMouseLeave={(e) => e.target.style.background = 'none'}
                        >
                            ✏️ Edit
                        </button>
                    )}
                </div>
                {isEditingBio ? (
                    <div>
                        <textarea
                            value={editedBio}
                            onChange={(e) => setEditedBio(e.target.value)}
                            rows="4"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem',
                                fontFamily: 'inherit',
                                resize: 'vertical',
                                marginBottom: '12px'
                            }}
                        />
                        <div style={{ display: 'flex', gap: '8px' }}>
                            <button onClick={handleSaveBio} style={{ padding: '8px 16px', borderRadius: '4px', background: 'black', color: 'white', border: 'none', cursor: 'pointer' }}>Save</button>
                            <button onClick={() => setIsEditingBio(false)} style={{ padding: '8px 16px', borderRadius: '4px', background: 'var(--bg-secondary)', border: '1px solid var(--border-light)', cursor: 'pointer' }}>Cancel</button>
                        </div>
                    </div>
                ) : (
                    <p style={{ color: user?.bio ? 'inherit' : 'var(--text-muted)', lineHeight: 1.6 }}>
                        {user?.bio || "No bio added yet. Click edit to add one!"}
                    </p>
                )}
            </div>

            {/* Sections */}
            <div className="grid-2">
                <div className="card">
                    <div className="section-header">
                        <h3 className="section-title" style={{ fontSize: '1rem' }}>Active Projects</h3>
                    </div>
                    <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '24px 0' }}>
                        No active projects
                    </p>
                </div>

                <div className="card">
                    <div className="section-header">
                        <h3 className="section-title" style={{ fontSize: '1rem' }}>Purchase History</h3>
                    </div>
                    <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '24px 0' }}>
                        No recent purchases
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Profile;
