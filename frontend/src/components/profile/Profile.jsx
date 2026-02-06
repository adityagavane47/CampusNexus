/**
 * CampusNexus - Profile Component
 * User profile with Hustle Score and stats
 */
import { useState, useEffect } from 'react';
import { usePeraWallet } from '../../hooks/usePeraWallet';
import { getAccountBalance, getCurrentNetwork } from '../../services/algorand';

export function Profile() {
    const { isConnected, accountAddress, truncateAddress } = usePeraWallet();
    const [balance, setBalance] = useState(0);
    const [hustleScore, setHustleScore] = useState(100); // Base score
    const [stats, setStats] = useState({
        projectsCompleted: 3,
        endorsements: 7,
        itemsSold: 2,
    });

    useEffect(() => {
        if (isConnected && accountAddress) {
            loadAccountInfo();
        }
    }, [isConnected, accountAddress]);

    const loadAccountInfo = async () => {
        try {
            const bal = await getAccountBalance(accountAddress);
            setBalance(bal);
        } catch (err) {
            console.error('Failed to load account info:', err);
        }
    };

    if (!isConnected) {
        return (
            <div className="text-center py-20">
                <span className="text-6xl">🔗</span>
                <h3 className="text-2xl font-bold text-white mt-4">Connect Your Wallet</h3>
                <p className="text-slate-400 mt-2">Connect your Pera Wallet to view your profile</p>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Profile Header */}
            <div className="glass-card p-6">
                <div className="flex items-center gap-6">
                    {/* Avatar */}
                    <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-4xl">
                        🎓
                    </div>

                    {/* Info */}
                    <div className="flex-1">
                        <h2 className="text-2xl font-bold text-white">VIT Pune Student</h2>
                        <p className="text-slate-400 font-mono mt-1">{accountAddress}</p>
                        <div className="flex items-center gap-4 mt-3">
                            <span className="flex items-center gap-1 text-sm text-slate-400">
                                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                {getCurrentNetwork()}
                            </span>
                            <span className="text-emerald-400 font-semibold">
                                {balance.toFixed(2)} ALGO
                            </span>
                        </div>
                    </div>

                    {/* Hustle Score */}
                    <div className="text-center">
                        <div className="w-24 h-24 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
                            <span className="text-3xl font-bold text-white">{hustleScore}</span>
                        </div>
                        <p className="text-sm text-slate-400 mt-2">Hustle Score</p>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-4">
                <div className="glass-card p-5 text-center">
                    <p className="text-3xl font-bold text-indigo-400">{stats.projectsCompleted}</p>
                    <p className="text-slate-400 text-sm mt-1">Projects Completed</p>
                </div>
                <div className="glass-card p-5 text-center">
                    <p className="text-3xl font-bold text-purple-400">{stats.endorsements}</p>
                    <p className="text-slate-400 text-sm mt-1">Endorsements</p>
                </div>
                <div className="glass-card p-5 text-center">
                    <p className="text-3xl font-bold text-emerald-400">{stats.itemsSold}</p>
                    <p className="text-slate-400 text-sm mt-1">Items Sold</p>
                </div>
            </div>

            {/* Skills Section */}
            <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-white mb-4">🎯 Verified Skills</h3>
                <div className="flex flex-wrap gap-2">
                    {['React', 'Python', 'Arduino', 'Machine Learning', 'FastAPI', 'Solidity'].map(skill => (
                        <span
                            key={skill}
                            className="px-4 py-2 bg-indigo-500/20 text-indigo-300 rounded-full border border-indigo-500/30"
                        >
                            {skill}
                        </span>
                    ))}
                </div>
            </div>

            {/* Recent Activity */}
            <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-white mb-4">📋 Recent Activity</h3>
                <div className="space-y-3">
                    <div className="flex items-center gap-3 text-sm">
                        <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">✅</span>
                        <span className="text-slate-300">Completed "IoT Dashboard" project</span>
                        <span className="text-slate-500 ml-auto">2 days ago</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                        <span className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">👍</span>
                        <span className="text-slate-300">Received endorsement for Python</span>
                        <span className="text-slate-500 ml-auto">5 days ago</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                        <span className="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center">🛒</span>
                        <span className="text-slate-300">Sold Arduino Kit for 15 ALGO</span>
                        <span className="text-slate-500 ml-auto">1 week ago</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;
