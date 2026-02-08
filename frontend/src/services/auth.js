/**
 * CampusNexus - Authentication Service
 * Handles OAuth login, token management, and user sessions
 */

const API_BASE_URL = 'http://localhost:8000/api';

export const authService = {
    /**
     * Initiate Google OAuth login
     */
    loginWithGoogle: () => {
        window.location.href = `${API_BASE_URL}/oauth/google/login`;
    },

    /**
     * Initiate GitHub OAuth login
     */
    loginWithGithub: () => {
        window.location.href = `${API_BASE_URL}/oauth/github/login`;
    },

    /**
     * Store authentication token
     */
    setToken: (token) => {
        localStorage.setItem('auth_token', token);
    },

    /**
     * Get authentication token
     */
    getToken: () => {
        return localStorage.getItem('auth_token');
    },

    /**
     * Remove authentication token
     */
    removeToken: () => {
        localStorage.removeItem('auth_token');
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated: () => {
        const token = authService.getToken();
        if (!token) return false;

        try {
            // Decode JWT token to check expiration
            const payload = JSON.parse(atob(token.split('.')[1]));
            const expiry = payload.exp * 1000; // Convert to milliseconds
            return Date.now() < expiry;
        } catch (e) {
            return false;
        }
    },

    /**
     * Get current user from token
     */
    getCurrentUser: () => {
        const token = authService.getToken();
        if (!token) return null;

        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return {
                id: payload.sub,
                email: payload.email,
                college: payload.college,
            };
        } catch (e) {
            return null;
        }
    },

    /**
     * Fetch full user profile
     */
    fetchUserProfile: async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/oauth/me?user_id=${userId}`);
            if (!response.ok) throw new Error('Failed to fetch profile');
            return await response.json();
        } catch (error) {
            console.error(error);
            return null;
        }
    },

    /**
     * Update user profile
     */
    updateProfile: async (userId, profileData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/oauth/profile?user_id=${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(profileData),
            });
            if (!response.ok) throw new Error('Failed to update profile');
            return await response.json();
        } catch (error) {
            console.error(error);
            throw error;
        }
    },

    /**
     * Upload profile picture
     */
    uploadProfilePicture: async (userId, imageData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/oauth/upload-profile-picture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, image_data: imageData }),
            });
            if (!response.ok) throw new Error('Failed to upload profile picture');
            return await response.json();
        } catch (error) {
            console.error(error);
            throw error;
        }
    },

    /**
     * Logout user
     */
    logout: () => {
        authService.removeToken();
        window.location.href = '/';
    },
};
