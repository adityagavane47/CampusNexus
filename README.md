# CampusNexus

> 🎓 Decentralized LinkedIn & Marketplace for VIT Pune on Algorand Blockchain

## Features

### Track 1: Finance
- **Milestone-Based Escrow** - Secure freelancing payments with milestone releases
- **P2P Marketplace** - Buy/sell Arduino kits, books, and equipment

### Track 2: AI/Automation
- **AI Skill-Matcher** - Match students with relevant opportunities
- **Hustle Score (SBT)** - On-chain reputation via Soulbound Tokens

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python (FastAPI) |
| Frontend | React + Tailwind CSS |
| Smart Contracts | Algorand Python (AlgoKit) |
| Wallet | Pera Wallet |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- [AlgoKit](https://developer.algorand.org/docs/get-started/algokit/)
- Docker

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# API Docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
```

## Project Structure
```
├── backend/         # FastAPI backend
├── frontend/        # React + Tailwind frontend
└── contracts/       # Algorand Python smart contracts
```

## License
MIT
