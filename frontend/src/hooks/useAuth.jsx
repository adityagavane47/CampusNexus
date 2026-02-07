/**
 * CampusNexus - Authentication Hook
 * React hook for managing authentication state
 */
import { useState, useEffect } from 'react';
import { authService } from '../services/auth';

export function useAuth() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuth = async () => {
            let token = authService.getToken();

            // Check for OAuth callback with token
            const urlParams = new URLSearchParams(window.location.search);
            const oauthToken = urlParams.get('token');
            const error = urlParams.get('error');

            if (oauthToken) {
                authService.setToken(oauthToken);
                token = oauthToken;
                window.history.replaceState({}, document.title, window.location.pathname);
            } else if (error) {
                console.error('OAuth error:', error);
                alert('Authentication failed. Please try again.');
                window.history.replaceState({}, document.title, window.location.pathname);
                setLoading(false);
                return;
            }

            if (!token || !authService.isAuthenticated()) {
                setLoading(false);
                return;
            }

            setIsAuthenticated(true);

            // Get basic info from token
            const basicUser = authService.getCurrentUser();

            if (basicUser) {
                try {
                    // Fetch full profile to get year/branch
                    const profile = await authService.fetchUserProfile(basicUser.id);
                    setUser(profile || basicUser);
                } catch (err) {
                    console.error("Failed to load profile", err);
                    setUser(basicUser);
                }
            }

            setLoading(false);
        };

        checkAuth();
    }, []);

    const logout = () => {
        authService.logout();
        setUser(null);
        setIsAuthenticated(false);
    };

    return {
        user,
        loading,
        isAuthenticated,
        logout,
    };
}
