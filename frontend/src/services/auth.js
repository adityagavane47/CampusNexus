const API_BASE_URL = 'http://localhost:8000/api';

export const authService = {
    
    loginWithGoogle: () => {
        window.location.href = `${API_BASE_URL}/oauth/google/login`;
    },

    
    loginWithGithub: () => {
        window.location.href = `${API_BASE_URL}/oauth/github/login`;
    },

    
    setToken: (token) => {
        localStorage.setItem('auth_token', token);
    },

    
    getToken: () => {
        return localStorage.getItem('auth_token');
    },

    
    removeToken: () => {
        localStorage.removeItem('auth_token');
    },

    
    isAuthenticated: () => {
        const token = authService.getToken();
        if (!token) return false;

        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const expiry = payload.exp * 1000;
            return Date.now() < expiry;
        } catch (e) {
            return false;
        }
    },

    
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

    
    logout: () => {
        authService.removeToken();
        window.location.href = '/';
    },
};
