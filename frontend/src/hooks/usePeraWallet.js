/**
 * CampusNexus - Pera Wallet Hook
 * Custom React hook for Algorand wallet integration
 */
import { useState, useEffect, useCallback } from 'react';

// Lazy load Pera Wallet to avoid SSR issues
let peraWallet = null;

const getPeraWallet = async () => {
    if (!peraWallet) {
        try {
            const { PeraWalletConnect } = await import('@perawallet/connect');
            peraWallet = new PeraWalletConnect({
                shouldShowSignTxnToast: true,
            });
        } catch (err) {
            console.error('Failed to load Pera Wallet:', err);
            throw err;
        }
    }
    return peraWallet;
};

export function usePeraWallet() {
    const [accountAddress, setAccountAddress] = useState(null);
    const [isConnecting, setIsConnecting] = useState(false);
    const [isInitialized, setIsInitialized] = useState(false);
    const [error, setError] = useState(null);

    // Initialize and check for existing connection
    useEffect(() => {
        const init = async () => {
            try {
                const wallet = await getPeraWallet();

                const accounts = await wallet.reconnectSession();
                if (accounts.length > 0) {
                    setAccountAddress(accounts[0]);
                }

                // Disconnect listener
                wallet.connector?.on('disconnect', handleDisconnect);

                setIsInitialized(true);
            } catch (err) {
                console.log('Wallet init error (this is normal on first load):', err);
                setIsInitialized(true);
            }
        };

        init();

        return () => {
            if (peraWallet?.connector) {
                peraWallet.connector.off('disconnect', handleDisconnect);
            }
        };
    }, []);

    const handleDisconnect = useCallback(() => {
        setAccountAddress(null);
        setError(null);
    }, []);

    const connect = useCallback(async () => {
        setIsConnecting(true);
        setError(null);

        try {
            const wallet = await getPeraWallet();
            const accounts = await wallet.connect();

            if (accounts.length > 0) {
                setAccountAddress(accounts[0]);
                return accounts[0];
            }
        } catch (err) {
            if (err?.data?.type !== 'CONNECT_MODAL_CLOSED') {
                setError(err.message || 'Failed to connect wallet');
                console.error('Wallet connection error:', err);
            }
        } finally {
            setIsConnecting(false);
        }

        return null;
    }, []);

    const disconnect = useCallback(async () => {
        try {
            const wallet = await getPeraWallet();
            await wallet.disconnect();
            setAccountAddress(null);
        } catch (err) {
            console.error('Disconnect error:', err);
        }
    }, []);

    const signTransaction = useCallback(async (txn) => {
        if (!accountAddress) {
            throw new Error('Wallet not connected');
        }

        try {
            const wallet = await getPeraWallet();
            const signedTxn = await wallet.signTransaction([[{ txn }]]);
            return signedTxn;
        } catch (err) {
            console.error('Sign transaction error:', err);
            throw err;
        }
    }, [accountAddress]);

    const truncateAddress = (address) => {
        if (!address) return '';
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    };

    return {
        accountAddress,
        isConnecting,
        isConnected: !!accountAddress,
        isInitialized,
        error,
        connect,
        disconnect,
        signTransaction,
        truncateAddress: () => truncateAddress(accountAddress),
    };
}

export default usePeraWallet;
