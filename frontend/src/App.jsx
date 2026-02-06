/**
 * CampusNexus - Main App Component
 * Decentralized LinkedIn & Marketplace for VIT Pune
 */
import { useState } from 'react';
import { WalletConnect } from './components/wallet/WalletConnect';
import { ProjectFeed } from './components/feed/ProjectFeed';
import { CreateProjectModal } from './components/feed/CreateProjectModal';
import { Marketplace } from './components/marketplace/Marketplace';
import { Profile } from './components/profile/Profile';
import { getCurrentNetwork } from './services/algorand';
import './index.css';

function App() {
    const [activeTab, setActiveTab] = useState('feed');
    const [showCreateModal, setShowCreateModal] = useState(false);

    const tabs = [
        { id: 'feed', label: '🚀 Projects', icon: '💼' },
        { id: 'marketplace', label: '🛒 Marketplace', icon: '📦' },
        { id: 'profile', label: '👤 Profile', icon: '🎯' },
    ];

    const handleCreateProject = async (projectData) => {
        console.log('Creating project:', projectData);
        // TODO: Call backend API and create escrow
        alert('Project created! (Demo mode - backend integration pending)');
    };

    return (
        <div className="min-h-screen bg-[#0f0f23]">
            {/* Navigation */}
            <nav className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-slate-800">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo */}
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-xl font-bold">
                                CN
                            </div>
                            <div>
                                <h1 className="text-lg font-bold text-white">CampusNexus</h1>
                                <p className="text-xs text-indigo-400">VIT Pune • {getCurrentNetwork()}</p>
                            </div>
                        </div>

                        {/* Tabs */}
                        <div className="hidden md:flex items-center gap-1 bg-slate-800/50 rounded-xl p-1">
                            {tabs.map(tab => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`
                    px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                    ${activeTab === tab.id
                                            ? 'bg-indigo-500 text-white'
                                            : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
                                        }
                  `}
                                >
                                    {tab.label}
                                </button>
                            ))}
                        </div>

                        {/* Wallet Connect */}
                        <WalletConnect />
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <div className="relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 via-purple-600/10 to-transparent"></div>
                <div className="absolute top-20 left-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl"></div>
                <div className="absolute top-40 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>

                <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="text-center">
                        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                            <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                                Build. Earn. Connect.
                            </span>
                        </h2>
                        <p className="text-xl text-slate-400 max-w-2xl mx-auto">
                            The decentralized platform for VIT Pune students to find freelance gigs,
                            trade equipment, and build their on-chain reputation.
                        </p>

                        {/* Stats */}
                        <div className="flex justify-center gap-8 mt-8">
                            <div className="text-center">
                                <p className="text-3xl font-bold text-indigo-400">150+</p>
                                <p className="text-sm text-slate-500">Active Projects</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-purple-400">500+</p>
                                <p className="text-sm text-slate-500">Students</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-cyan-400">25K</p>
                                <p className="text-sm text-slate-500">ALGO Traded</p>
                            </div>
                        </div>

                        {/* CTA Button */}
                        {activeTab === 'feed' && (
                            <button
                                onClick={() => setShowCreateModal(true)}
                                className="mt-8 btn-primary text-lg px-8 py-3"
                            >
                                + Post a Project
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {activeTab === 'feed' && <ProjectFeed />}
                {activeTab === 'marketplace' && <Marketplace />}
                {activeTab === 'profile' && <Profile />}
            </main>

            {/* Footer */}
            <footer className="border-t border-slate-800 mt-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                        <p className="text-slate-500 text-sm">
                            Built with 💜 for VIT Pune on Algorand
                        </p>
                        <div className="flex items-center gap-4">
                            <span className="flex items-center gap-2 text-sm text-slate-400">
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                {getCurrentNetwork()}
                            </span>
                            <a
                                href="https://github.com/adityagavane47/CampusNexus"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                GitHub
                            </a>
                        </div>
                    </div>
                </div>
            </footer>

            {/* Create Project Modal */}
            <CreateProjectModal
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onSubmit={handleCreateProject}
            />
        </div>
    );
}

export default App;
