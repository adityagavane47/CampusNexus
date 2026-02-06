/**
 * CampusNexus - Project Feed Component
 * Displays student project/gig opportunities
 */
import { useState, useEffect } from 'react';

// Mock data for initial display
const mockProjects = [
    {
        id: 1,
        title: "Build IoT Dashboard for Smart Campus",
        description: "Need a React dashboard to visualize sensor data from Arduino-based IoT devices placed around campus.",
        skills_required: ["React", "Arduino", "IoT", "REST API"],
        budget_algo: 50,
        deadline: "2026-03-01",
        status: "open",
        applications_count: 3,
        creator_address: "VIT7...X3K2",
    },
    {
        id: 2,
        title: "Machine Learning Model for Attendance",
        description: "Develop a facial recognition attendance system using Python and OpenCV for classroom automation.",
        skills_required: ["Python", "ML", "OpenCV", "TensorFlow"],
        budget_algo: 100,
        deadline: "2026-02-28",
        status: "open",
        applications_count: 7,
        creator_address: "VIT9...M4P1",
    },
    {
        id: 3,
        title: "Mobile App for Campus Events",
        description: "Create a cross-platform mobile app for VIT Pune events, clubs, and notifications using React Native.",
        skills_required: ["React Native", "Firebase", "UI/UX"],
        budget_algo: 75,
        deadline: "2026-03-15",
        status: "open",
        applications_count: 5,
        creator_address: "VIT2...J8N5",
    },
];

export function ProjectFeed() {
    const [projects, setProjects] = useState(mockProjects);
    const [filter, setFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    const filteredProjects = projects.filter(project => {
        const matchesSearch = project.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            project.skills_required.some(skill =>
                skill.toLowerCase().includes(searchQuery.toLowerCase())
            );
        return matchesSearch;
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                        🚀 Project Feed
                    </h2>
                    <p className="text-slate-400 mt-1">Find opportunities or post your own gig</p>
                </div>

                {/* Search */}
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Search by skill or title..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="
              w-full md:w-80 px-4 py-2.5 pl-10
              bg-slate-800/50 border border-slate-700 rounded-xl
              text-white placeholder-slate-500
              focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20
              transition-all duration-200
            "
                    />
                    <svg
                        className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
            </div>

            {/* Project Cards */}
            <div className="grid gap-4">
                {filteredProjects.map((project, index) => (
                    <div
                        key={project.id}
                        className="
              glass-card p-6 animate-fade-in
              hover:border-indigo-500/50
            "
                        style={{ animationDelay: `${index * 100}ms` }}
                    >
                        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
                            {/* Content */}
                            <div className="flex-1">
                                <div className="flex items-start gap-3">
                                    <span className="text-2xl">💼</span>
                                    <div>
                                        <h3 className="text-lg font-semibold text-white hover:text-indigo-400 transition-colors cursor-pointer">
                                            {project.title}
                                        </h3>
                                        <p className="text-slate-400 text-sm mt-1 line-clamp-2">
                                            {project.description}
                                        </p>
                                    </div>
                                </div>

                                {/* Skills */}
                                <div className="flex flex-wrap gap-2 mt-4">
                                    {project.skills_required.map(skill => (
                                        <span
                                            key={skill}
                                            className="
                        px-3 py-1 text-xs font-medium
                        bg-indigo-500/20 text-indigo-300 
                        rounded-full border border-indigo-500/30
                      "
                                        >
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            {/* Stats & Actions */}
                            <div className="flex lg:flex-col items-center lg:items-end gap-4">
                                {/* Budget */}
                                <div className="text-right">
                                    <p className="text-2xl font-bold text-emerald-400">
                                        {project.budget_algo} ALGO
                                    </p>
                                    <p className="text-xs text-slate-500">Budget</p>
                                </div>

                                {/* Meta */}
                                <div className="flex items-center gap-4 text-sm text-slate-400">
                                    <span className="flex items-center gap-1">
                                        👥 {project.applications_count} applied
                                    </span>
                                    <span className="flex items-center gap-1">
                                        ⏰ {new Date(project.deadline).toLocaleDateString()}
                                    </span>
                                </div>

                                {/* Apply Button */}
                                <button className="btn-primary text-sm">
                                    Apply Now
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Empty State */}
            {filteredProjects.length === 0 && (
                <div className="text-center py-12">
                    <span className="text-4xl">🔍</span>
                    <p className="text-slate-400 mt-4">No projects found matching your search</p>
                </div>
            )}
        </div>
    );
}

export default ProjectFeed;
