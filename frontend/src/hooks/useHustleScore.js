import { useState, useEffect } from 'react';
import { hustleService } from '../services/hustle';

export function useHustleScore(walletAddress) {
    const [score, setScore] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [initialized, setInitialized] = useState(false);

    useEffect(() => {
        let isMounted = true;

        async function fetchScore() {
            if (!walletAddress) {
                setScore(0);
                setInitialized(false);
                return;
            }

            setLoading(true);
            setError(null);

            try {
                const data = await hustleService.getScore(walletAddress);

                if (isMounted) {
                    setScore(data.score);
                    setInitialized(data.initialized);
                }
            } catch (err) {
                if (isMounted) {
                    console.error('Failed to fetch Hustle Score:', err);
                    setError(err.message);
                    setScore(0);
                    setInitialized(false);
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        fetchScore();

        return () => {
            isMounted = false;
        };
    }, [walletAddress]);

    
    const refreshScore = async () => {
        if (!walletAddress) return;

        setLoading(true);
        setError(null);

        try {
            const data = await hustleService.getScore(walletAddress);
            setScore(data.score);
            setInitialized(data.initialized);
        } catch (err) {
            console.error('Failed to refresh Hustle Score:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return {
        score,
        loading,
        error,
        initialized,
        refreshScore
    };
}

export default useHustleScore;
