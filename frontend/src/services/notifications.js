/**
 * CampusNexus - Notifications API Service
 * Handles fetching and updating notifications
 */

const API_BASE_URL = 'http://localhost:8000/api';

export const notificationsService = {
    /**
     * Get all notifications for a specific user
     */
    getNotifications: async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/notifications/?user_id=${userId}`);
            if (!response.ok) throw new Error('Failed to fetch notifications');

            return await response.json();
        } catch (error) {
            console.error('Error fetching notifications:', error);
            throw error;
        }
    },

    /**
     * Get unread notification count
     */
    getUnreadCount: async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/notifications/unread-count?user_id=${userId}`);
            if (!response.ok) throw new Error('Failed to fetch unread count');

            return await response.json();
        } catch (error) {
            console.error('Error fetching unread count:', error);
            // Return 0 on error to avoid breaking UI
            return { count: 0 };
        }
    },

    /**
     * Mark a notification as read
     */
    markAsRead: async (notificationId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
                method: 'PUT',
            });

            if (!response.ok) throw new Error('Failed to mark notification as read');

            return await response.json();
        } catch (error) {
            console.error('Error marking notification as read:', error);
            throw error;
        }
    },
};
