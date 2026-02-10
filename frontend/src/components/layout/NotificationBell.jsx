
import { useState, useEffect, useRef } from 'react';
import { notificationsService } from '../../services/notifications';
import { useAuth } from '../../hooks/useAuth';

export function NotificationBell() {
    const { user } = useAuth();
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        if (user) {
            fetchUnreadCount();
            // Poll for notifications every 30 seconds
            const interval = setInterval(fetchUnreadCount, 30000);
            return () => clearInterval(interval);
        }
    }, [user]);

    useEffect(() => {
        // Close dropdown when clicking outside
        function handleClickOutside(event) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [dropdownRef]);

    const fetchUnreadCount = async () => {
        if (!user) return;
        try {
            const data = await notificationsService.getUnreadCount(user.id);
            setUnreadCount(data.count);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchNotifications = async () => {
        if (!user) return;
        try {
            const data = await notificationsService.getNotifications(user.id);
            setNotifications(data);
        } catch (error) {
            console.error(error);
        }
    };

    const handleBellClick = () => {
        if (!isOpen) {
            fetchNotifications();
        }
        setIsOpen(!isOpen);
    };

    const handleMarkAsRead = async (notification) => {
        if (notification.is_read) return;
        try {
            await notificationsService.markAsRead(notification.id);
            // Update local state
            setNotifications(prev => prev.map(n =>
                n.id === notification.id ? { ...n, is_read: true } : n
            ));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (error) {
            console.error(error);
        }
    };

    if (!user) return null;

    return (
        <div className="notification-bell-container" ref={dropdownRef} style={{ position: 'relative' }}>
            <button
                onClick={handleBellClick}
                style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: '8px',
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text-primary)'
                }}
            >
                <span style={{ fontSize: '1.25rem' }}>🔔</span>
                {unreadCount > 0 && (
                    <span style={{
                        position: 'absolute',
                        top: '0',
                        right: '0',
                        backgroundColor: 'var(--accent-primary)', // Assuming red/brand color
                        color: 'white',
                        borderRadius: '50%',
                        width: '18px',
                        height: '18px',
                        fontSize: '0.75rem',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 'bold',
                        border: '2px solid var(--bg-primary)'
                    }}>
                        {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                )}
            </button>

            {isOpen && (
                <div style={{
                    position: 'absolute',
                    top: '100%',
                    right: '0',
                    width: '320px',
                    maxHeight: '400px',
                    overflowY: 'auto',
                    backgroundColor: 'var(--bg-primary)',
                    border: '1px solid var(--border-light)',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                    zIndex: 1000,
                    marginTop: '8px'
                }}>
                    <div style={{
                        padding: '12px 16px',
                        borderBottom: '1px solid var(--border-light)',
                        fontWeight: 600
                    }}>
                        Notifications
                    </div>

                    {notifications.length === 0 ? (
                        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                            No notifications
                        </div>
                    ) : (
                        <div style={{ padding: '0' }}>
                            {notifications.map(notification => (
                                <div
                                    key={notification.id}
                                    onClick={() => handleMarkAsRead(notification)}
                                    style={{
                                        padding: '12px 16px',
                                        borderBottom: '1px solid var(--border-light)',
                                        cursor: 'pointer',
                                        backgroundColor: notification.is_read ? 'transparent' : 'var(--bg-secondary)',
                                        transition: 'background-color 0.2s'
                                    }}
                                >
                                    <div style={{ fontWeight: 500, marginBottom: '4px', fontSize: '0.9rem' }}>
                                        {notification.title}
                                    </div>
                                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                                        {notification.message}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                                        {new Date(notification.created_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
