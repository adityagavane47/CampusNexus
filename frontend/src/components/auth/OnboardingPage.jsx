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
        skills: user?.skills || [],
        bio: user?.bio || '',
    });
    const [profilePicture, setProfilePicture] = useState(user?.profile_picture || null);
    const [currentSkill, setCurrentSkill] = useState('');

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

    const handleProfilePictureChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setProfilePicture(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleAddSkill = () => {
        if (currentSkill.trim() && !formData.skills.includes(currentSkill.trim())) {
            setFormData(prev => ({
                ...prev,
                skills: [...prev.skills, currentSkill.trim()]
            }));
            setCurrentSkill('');
        }
    };

    const handleRemoveSkill = (skillToRemove) => {
        setFormData(prev => ({
            ...prev,
            skills: prev.skills.filter(skill => skill !== skillToRemove)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Upload profile picture if provided
            if (profilePicture && profilePicture !== user?.profile_picture) {
                await authService.uploadProfilePicture(user.id, profilePicture);
            }

            await authService.updateProfile(user.id, {
                name: formData.name,
                age: parseInt(formData.age),
                year: formData.year,
                branch: formData.branch,
                skills: formData.skills,
                profile_picture: profilePicture,
                bio: formData.bio
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

                    {/* Profile Picture Upload */}
                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Profile Picture</label>
                        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
                            {profilePicture && (
                                <img
                                    src={profilePicture}
                                    alt="Profile preview"
                                    style={{
                                        width: '80px',
                                        height: '80px',
                                        borderRadius: '50%',
                                        objectFit: 'cover',
                                        border: '2px solid var(--border-light)'
                                    }}
                                />
                            )}
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handleProfilePictureChange}
                                style={{
                                    padding: '8px',
                                    fontSize: '0.875rem'
                                }}
                            />
                        </div>
                    </div>

                    {/* Skills Input */}
                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>Skills</label>
                        <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                            <input
                                type="text"
                                value={currentSkill}
                                onChange={(e) => setCurrentSkill(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
                                placeholder="e.g., React, Python, Design"
                                className="input-field"
                                style={{
                                    flex: 1,
                                    padding: '12px',
                                    borderRadius: '8px',
                                    border: '1px solid var(--border-light)',
                                    fontSize: '1rem'
                                }}
                            />
                            <button
                                type="button"
                                onClick={handleAddSkill}
                                style={{
                                    padding: '12px 20px',
                                    borderRadius: '8px',
                                    backgroundColor: 'var(--bg-secondary)',
                                    border: '1px solid var(--border-light)',
                                    cursor: 'pointer',
                                    fontWeight: 500
                                }}
                            >
                                Add
                            </button>
                        </div>
                        {formData.skills.length > 0 && (
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                                {formData.skills.map((skill, index) => (
                                    <span
                                        key={index}
                                        style={{
                                            padding: '6px 12px',
                                            backgroundColor: 'black',
                                            color: 'white',
                                            borderRadius: '20px',
                                            fontSize: '0.875rem',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '6px'
                                        }}
                                    >
                                        {skill}
                                        <button
                                            type="button"
                                            onClick={() => handleRemoveSkill(skill)}
                                            style={{
                                                background: 'none',
                                                border: 'none',
                                                color: 'white',
                                                cursor: 'pointer',
                                                padding: '0',
                                                fontSize: '1.2rem',
                                                lineHeight: 1
                                            }}
                                        >
                                            ×
                                        </button>
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Bio/About Me */}
                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: 500, textAlign: 'left' }}>About Me</label>
                        <textarea
                            name="bio"
                            value={formData.bio}
                            onChange={handleChange}
                            placeholder="Tell us about yourself..."
                            rows="4"
                            className="input-field"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                fontSize: '1rem',
                                fontFamily: 'inherit',
                                resize: 'vertical'
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
