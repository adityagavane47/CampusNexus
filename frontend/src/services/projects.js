/**
 * CampusNexus - Projects API Service
 * Handles all project-related API calls
 */

const API_BASE_URL = 'http://localhost:8000/api';

export const projectsService = {
    /**
     * Get all projects with optional filters
     */
    getProjects: async (filters = {}) => {
        try {
            const params = new URLSearchParams();

            if (filters.skill) params.append('skill', filters.skill);
            if (filters.min_budget) params.append('min_budget', filters.min_budget);
            if (filters.status) params.append('status', filters.status);
            if (filters.creator_id) params.append('creator_id', filters.creator_id);

            const queryString = params.toString();
            const url = `${API_BASE_URL}/feed${queryString ? `?${queryString}` : ''}`;

            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch projects');

            return await response.json();
        } catch (error) {
            console.error('Error fetching projects:', error);
            throw error;
        }
    },

    /**
     * Get a specific project by ID
     */
    getProject: async (projectId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/feed/${projectId}`);
            if (!response.ok) throw new Error('Project not found');

            return await response.json();
        } catch (error) {
            console.error('Error fetching project:', error);
            throw error;
        }
    },

    /**
     * Create a new project
     */
    createProject: async (projectData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/feed`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(projectData),
            });

            if (!response.ok) throw new Error('Failed to create project');

            return await response.json();
        } catch (error) {
            console.error('Error creating project:', error);
            throw error;
        }
    },

    /**
     * Apply to a project
     */
    applyToProject: async (projectId, applicantId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/feed/${projectId}/apply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ applicant_id: applicantId }),
            });

            if (!response.ok) throw new Error('Failed to apply to project');

            return await response.json();
        } catch (error) {
            console.error('Error applying to project:', error);
            throw error;
        }
    },
};
