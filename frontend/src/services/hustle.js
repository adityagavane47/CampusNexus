/**
 * Hustle Score API Service
 * Handles API calls for querying student reputation scores
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const hustleService = {
    /**
     * Get Hustle Score for a wallet address
     * @param {string} walletAddress - Algorand wallet address
     * @returns {Promise<{wallet_address: string, score: number, initialized: boolean}>}
     */
    async getScore(walletAddress) {
        if (!walletAddress) {
            throw new Error('Wallet address is required');
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/hustle/score/${walletAddress}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching Hustle Score:', error);
            throw error;
        }
    },

    /**
     * Initialize a student's Hustle Score (creates box storage)
     * @param {string} walletAddress - Algorand wallet address
     * @returns {Promise<{message: string, wallet_address: string}>}
     */
    async initialize(walletAddress) {
        if (!walletAddress) {
            throw new Error('Wallet address is required');
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/hustle/initialize/${walletAddress}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error initializing Hustle Score:', error);
            throw error;
        }
    },

    /**
     * Manually add reputation points (admin only in production)
     * @param {string} walletAddress - Algorand wallet address
     * @param {number} points - Points to add (default 10)
     * @returns {Promise<{message: string, wallet_address: string, new_score: number, transaction_id: string}>}
     */
    async addPoints(walletAddress, points = 10) {
        if (!walletAddress) {
            throw new Error('Wallet address is required');
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/hustle/add-points/${walletAddress}?points=${points}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error adding reputation points:', error);
            throw error;
        }
    }
};

export default hustleService;
