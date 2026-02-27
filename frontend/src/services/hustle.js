const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const hustleService = {
    
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
