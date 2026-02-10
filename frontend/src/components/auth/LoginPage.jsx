/**
 * CampusNexus - Login Page
 * Beautiful OAuth authentication page with Google and GitHub
 */
import { useState } from 'react';
import { OAuthButton } from './OAuthButton';
import { authService } from '../../services/auth';

export function LoginPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGoogleLogin = async () => {
        try {
            setLoading(true);
            setError(null);

            // Check if OAuth is configured by making a test request
            const response = await fetch('http://localhost:8000/api/oauth/google/login', {
                method: 'GET',
                redirect: 'manual'  // Don't follow redirects automatically
            });

            // If we get a redirect (3xx status), OAuth is configured
            if (response.type === 'opaqueredirect' || response.status === 0) {
                authService.loginWithGoogle();
            } else if (response.status === 500) {
                setError('Google OAuth is not configured. Please set up OAuth credentials in the backend .env file. See OAUTH_SETUP.md for instructions.');
                setLoading(false);
            } else {
                authService.loginWithGoogle();
            }
        } catch (err) {
            setError('Unable to connect to the authentication server. Please make sure the backend is running.');
            setLoading(false);
        }
    };

    const handleGithubLogin = async () => {
        try {
            setLoading(true);
            setError(null);

            // Check if OAuth is configured
            const response = await fetch('http://localhost:8000/api/oauth/github/login', {
                method: 'GET',
                redirect: 'manual'
            });

            if (response.type === 'opaqueredirect' || response.status === 0) {
                authService.loginWithGithub();
            } else if (response.status === 500) {
                setError('GitHub OAuth is not configured. Please set up OAuth credentials in the backend .env file. See OAUTH_SETUP.md for instructions.');
                setLoading(false);
            } else {
                authService.loginWithGithub();
            }
        } catch (err) {
            setError('Unable to connect to the authentication server. Please make sure the backend is running.');
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            {/* Background with gradient */}
            <div className="login-background" />

            {/* Login Card */}
            <div className="login-card">
                {/* Logo */}
                <div className="login-logo">
                    <div className="logo-icon">CN</div>
                    <h1>CampusNexus</h1>
                    <p className="logo-subtitle">VIT Pune</p>
                </div>

                {/* Welcome Text */}
                <div className="login-header">
                    <h2>Welcome</h2>
                    <p>Sign in to access your campus ecosystem</p>
                </div>

                {/* Error Message */}
                {error && (
                    <div style={{
                        padding: '16px',
                        backgroundColor: '#fee',
                        border: '1px solid #fcc',
                        borderRadius: '8px',
                        marginBottom: '16px',
                        fontSize: '0.875rem',
                        color: '#c33',
                        lineHeight: '1.5'
                    }}>
                        <strong>⚠️ Setup Required:</strong><br />
                        {error}
                        <br /><br />
                        <strong>Quick Start:</strong> Use "Connect with Pera Wallet" below to skip OAuth setup for now.
                    </div>
                )}

                {/* OAuth Buttons */}
                <div className="login-buttons">
                    <OAuthButton
                        provider="google"
                        onClick={handleGoogleLogin}
                        disabled={loading}
                    />
                    <OAuthButton
                        provider="github"
                        onClick={handleGithubLogin}
                        disabled={loading}
                    />
                </div>



            </div>


        </div>
    );
}
