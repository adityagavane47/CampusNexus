/**
 * CampusNexus - Wallet Connect (Minimalist Design)
 */
import { usePeraWallet } from '../../hooks/usePeraWallet';

export function WalletConnect() {
    const {
        isConnected,
        accountAddress,
        connect,
        disconnect,
        isLoading,
        truncateAddress
    } = usePeraWallet();

    if (isConnected && accountAddress) {
        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
            }}>
                <div style={{
                    padding: '10px 16px',
                    backgroundColor: 'var(--bg-secondary)',
                    border: '1px solid var(--border-light)',
                    borderRadius: '4px',
                }}>
                    <span style={{
                        fontSize: '0.875rem',
                        fontFamily: 'monospace',
                        color: 'var(--text-primary)',
                    }}>
                        {truncateAddress(accountAddress)}
                    </span>
                </div>
                <button
                    onClick={disconnect}
                    style={{
                        padding: '10px 16px',
                        fontSize: '0.875rem',
                        fontWeight: 500,
                        backgroundColor: 'transparent',
                        border: '1px solid var(--border-light)',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        color: 'var(--text-muted)',
                        transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                        e.target.style.borderColor = 'var(--accent-error)';
                        e.target.style.color = 'var(--accent-error)';
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.borderColor = 'var(--border-light)';
                        e.target.style.color = 'var(--text-muted)';
                    }}
                >
                    Disconnect
                </button>
            </div>
        );
    }

    return (
        <button
            onClick={connect}
            disabled={isLoading}
            className="btn-primary"
            style={{ opacity: isLoading ? 0.7 : 1 }}
        >
            {isLoading ? 'Connecting...' : 'Connect Wallet'}
        </button>
    );
}

export default WalletConnect;
