# CampusNexus 🎓

> Decentralized LinkedIn & Marketplace for VIT Pune on Algorand Blockchain

## 🚀 Features

### Track 1: Finance
- **Milestone-Based Escrow** - Secure freelancing payments with milestone releases
- **P2P Marketplace** - Buy/sell Arduino kits, books, and equipment

### Track 2: AI/Automation
- **AI Skill-Matcher** - Match students with relevant opportunities
- **Hustle Score (SBT)** - On-chain reputation via Soulbound Tokens

## 📱 Platforms

| Platform | Status |
|----------|--------|
| Web | ✅ Ready |
| Android | ✅ Ready (Capacitor) |
| iOS | ✅ Ready (Capacitor) |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python (FastAPI) |
| Frontend | React + Tailwind CSS |
| Smart Contracts | Algorand Python (AlgoKit) |
| Wallet | Pera Wallet |
| Mobile | Capacitor |

## 🏃 Quick Start

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

### Frontend (Web)
```bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
```

### Mobile App (Android)
```bash
cd frontend
npm run build
npx cap sync android
npx cap open android
# Build APK in Android Studio
```

## 📁 Project Structure
```
├── backend/              # FastAPI backend
├── frontend/             # React + Tailwind + Capacitor
│   ├── android/          # Native Android project
│   └── src/              # React source
└── contracts/            # Algorand Python smart contracts
    └── campus-contracts/
```

## 🔐 Smart Contracts

- **MilestoneEscrow** - Freelancing milestone payments
- **HustleScore** - Soulbound reputation token

## 📄 License
MIT
