import { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { authService } from '../../services/auth';
import '../../index.css';

export function OnboardingPage({ onComplete }) {
    const { user } = useAuth();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: user?.name || '',
        age: user?.age || '',
        year: user?.year || '1st Year',
        branch: user?.branch || 'Computer Engineering',
    });

    useEffect(() => {
        if (user) {
            setFormData(prev => ({
                ...prev,
                name: user.name || prev.name,
                age: user.age || prev.age,
                year: user.year || prev.year,
                branch: user.branch || prev.branch
            }));
        }
    }, [user]);

    const handleChange = (e) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            await authService.updateProfile(user.id, {
                name: formData.name,
                age: parseInt(formData.age),
                year: formData.year,
                branch: formData.branch
            });
            onComplete();
        } catch (error) {
            console.error('Failed to update profile:', error);
            alert('Failed to save profile. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const branches = [
        'Computer Engineering',
        'Information Technology',
        'Electronics & Telecommunication',
        'Mechanical Engineering',
        'Civil Engineering',
        'Artificial Intelligence & Data Science'
    ];

    const years = ['1st Year', '2nd Year', '3rd Year', '4th Year'];

    return (
        <div className="login-page">
            <div className="login-background" />

            <div className="login-card" style={{ maxWidth: '480px' }}>
                <div className="login-header">
                    <h2>Complete Profile</h2>
                    <p>Tell us a bit about yourself</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Full Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            className="input-field"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem'
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Age</label>
                        <input
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            required
                            min="16"
                            max="30"
                            className="input-field"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem'
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Year</label>
                        <select
                            name="year"
                            value={formData.year}
                            onChange={handleChange}
                            className="input-field"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem',
                                backgroundColor: 'white'
                            }}
                        >
                            {years.map(y => <option key={y} value={y}>{y}</option>)}
                        </select>
                    </div>

                    <div style={{ marginBottom: '24px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Branch</label>
                        <select
                            name="branch"
                            value={formData.branch}
                            onChange={handleChange}
                            className="input-field"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem',
                                backgroundColor: 'white'
                            }}
                        >
                            {branches.map(b => <option key={b} value={b}>{b}</option>)}
                        </select>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-primary"
                        style={{
                            width: '100%',
                            padding: '14px',
                            borderRadius: '8px',
                            fontSize: '1rem',
                            fontWeight: 600,
                            backgroundColor: 'black',
                            color: 'white',
                            border: 'none',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Saving...' : 'Complete Profile'}
                    </button>
                </form>
            </div>
        </div>
    );
}
