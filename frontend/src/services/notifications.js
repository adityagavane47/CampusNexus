const API_BASE_URL = 'http://localhost:8000/api';

export const notificationsService = {
    
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

    
    getUnreadCount: async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/notifications/unread-count?user_id=${userId}`);
            if (!response.ok) throw new Error('Failed to fetch unread count');

            return await response.json();
        } catch (error) {
            console.error('Error fetching unread count:', error);
            return { count: 0 };
        }
    },

    
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
