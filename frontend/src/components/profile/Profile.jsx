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

    useEffect(() => {
        if (isConnected && accountAddress) {
            getAccountBalance(accountAddress).then(setBalance);
        }
    }, [isConnected, accountAddress]);

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
                    color: 'white'
                }}>
                    {user?.avatar ? <img src={user.avatar} style={{ width: '100%', height: '100%', borderRadius: '50%' }} /> : '👤'}
                </div>
                <div>
                    <h2 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>{user?.name || "Anonymous User"}</h2>
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
