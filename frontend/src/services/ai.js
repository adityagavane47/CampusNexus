/**
 * CampusNexus - AI Service
 * Endpoints for Track 2 features
 */

const API_URL = 'http://localhost:8000/api';

export async function matchProjects(skills) {
    try {
        const response = await fetch(`${API_URL}/ai/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ skills }),
        });

        if (!response.ok) {
            throw new Error('Failed to match projects');
        }

        return await response.json();
    } catch (error) {
        console.error('AI Match Error:', error);
        throw error;
    }
}
