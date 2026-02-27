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
            const response = await fetch('http://localhost:8000/api/oauth/google/login', {
                method: 'GET',
                redirect: 'manual',
            });
            if (response.type === 'opaqueredirect' || response.status === 0) {
                authService.loginWithGoogle();
            } else if (response.status === 500) {
                setError('Google OAuth is not configured. Set up credentials in the backend .env file.');
                setLoading(false);
            } else {
                authService.loginWithGoogle();
            }
        } catch {
            setError('Unable to connect to the authentication server. Make sure the backend is running.');
            setLoading(false);
        }
    };

    const handleGithubLogin = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await fetch('http://localhost:8000/api/oauth/github/login', {
                method: 'GET',
                redirect: 'manual',
            });
            if (response.type === 'opaqueredirect' || response.status === 0) {
                authService.loginWithGithub();
            } else if (response.status === 500) {
                setError('GitHub OAuth is not configured. Set up credentials in the backend .env file.');
                setLoading(false);
            } else {
                authService.loginWithGithub();
            }
        } catch {
            setError('Unable to connect to the authentication server. Make sure the backend is running.');
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            
            <div className="login-bg-gradient" />
            <div className="login-grid" />

            <div className="login-content">
                
                <div className="login-card">
                    
                    <div className="login-logo">
                        <div className="logo-icon">CN</div>
                        <h1>CampusNexus</h1>
                    </div>

                    
                    <div className="login-header">
                        <h2>Welcome back</h2>
                        <p>Sign in to access your campus ecosystem</p>
                    </div>

                    
                    {error && (
                        <div style={{
                            padding: '14px 16px',
                            background: 'rgba(255, 77, 109, 0.1)',
                            border: '1px solid rgba(255, 77, 109, 0.25)',
                            borderRadius: '10px',
                            marginBottom: '20px',
                            fontSize: '0.8125rem',
                            color: '#ff8099',
                            lineHeight: '1.5',
                        }}>
                            <strong>⚠️ Setup needed:</strong> {error}
                        </div>
                    )}

                    
                    <div className="login-buttons">
                        <OAuthButton provider="google" onClick={handleGoogleLogin} disabled={loading} />
                        <OAuthButton provider="github" onClick={handleGithubLogin} disabled={loading} />
                    </div>

                    
                    <div className="login-footer">
                        <p>By signing in you agree to our&nbsp;
                            <a href="#">Terms of Service</a> and&nbsp;
                            <a href="#">Privacy Policy</a>
                        </p>
                    </div>
                </div>

                
                <div className="login-features">
                    {[
                        { icon: '⚡', title: 'Live Projects', desc: 'Find real freelance gigs from fellow students' },
                        { icon: '🤖', title: 'AI Matching', desc: 'Get matched to projects that fit your skills' },
                        { icon: '🔐', title: 'Smart Escrow', desc: 'Payments secured on Algorand blockchain' },
                    ].map(f => (
                        <div key={f.title} className="feature-item">
                            <span className="feature-icon">{f.icon}</span>
                            <h3>{f.title}</h3>
                            <p>{f.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
