
## CampusNexus
### The Decentralized Ecosystem for Student Creators and Commerce

**CampusNexus** is a "Decentralized Ecosystem" and marketplace designed for the modern campus. It connects students through project collaboration and a secure marketplace, all powered by the speed and transparency of the **Algorand Blockchain** and automated by AI.

---

## Key Features

### Track 1: Future of Finance (Blockchain)
- **[Milestone-Based Escrow](contracts/campus-contracts/smart_contracts/escrow/contract.py)**: Secure peer-to-peer student freelancing. Payments are locked in smart contracts and released only when work is delivered.
- **P2P Marketplace**: Buy and sell used Arduino kits, sensors, and textbooks safely using ALGO.
- **Micro-Equity Tokens**: Team leads can issue ASAs (Algorand Standard Assets) to teammates to represent shares in a project's future success.

### Track 2: AI & Automation
- **[AI Skill-Matcher](backend/app/services/ai_matching.py)**: A smart backend that matches student profiles with project needs using NLP.
- **[Hustle-Score](contracts/campus-contracts/smart_contracts/hustle_score/contract.py)**: A verifiable reputation system. Earn Soulbound Tokens (SBTs) for successful collaborations, verified by AI feedback analysis.
- **[Automated Verification](backend/app/routers/ai.py)**: AI scans marketplace listings to verify item condition and suggest fair pricing.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Blockchain** | Algorand (Testnet) |
| **Smart Contracts** | Algorand Python 5.0 (AlgoKit) |
| **Backend** | Python (FastAPI) |
| **Frontend** | React.js + Tailwind CSS |
| **Wallet** | Pera Wallet / Defly |

---

## Architecture

![CampusNexus Workflow](Freelance%20Marketplace%20Flow-2026-02-06-202733.png)

- **Frontend**: React components for the Project Feed, Marketplace, and Profile.
- **Backend API**: FastAPI handles AI matching logic and metadata storage.
- **On-Chain Logic**: Algorand Smart Contracts handle all financial transactions and reputation minting.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- AlgoKit
- Docker (for LocalNet testing)

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/adityagavane47/CampusNexus.git
   cd campusnexus
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Local Blockchain**
   ```bash
   algokit localnet start
   ```

---

## Project Structure

```
CampusNexus/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Environment configuration
│   │   ├── routers/           # API endpoints
│   │   │   ├── oauth.py       # Google/GitHub OAuth authentication
│   │   │   ├── marketplace.py # Marketplace listings & purchases
│   │   │   ├── feed.py        # Project feed & applications
│   │   │   ├── ai.py          # AI matching & analysis
│   │   │   ├── hustle.py      # Hustle Score integration
│   │   │   └── notifications.py # User notifications
│   │   ├── services/          # Business logic
│   │   │   └── ai_matching.py # AI-powered skill matching
│   │   └── utils/             # Helper utilities
│   │       ├── database.py    # JSON database operations
│   │       └── ipfs.py        # IPFS integration (Pinata)
│   ├── data/                  # JSON data storage
│   │   ├── users.json
│   │   ├── projects.json
│   │   ├── marketplace.json
│   │   └── notifications.json
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── components/
│   │   │   ├── auth/          # Authentication UI
│   │   │   ├── feed/          # Project feed components
│   │   │   ├── marketplace/   # Marketplace UI
│   │   │   ├── profile/       # User profile
│   │   │   ├── wallet/        # Wallet connection
│   │   │   └── layout/        # Navigation, notifications
│   │   ├── hooks/             # Custom React hooks
│   │   │   ├── useAuth.jsx    # Authentication hook
│   │   │   ├── usePeraWallet.js # Pera Wallet integration
│   │   │   └── useEscrow.js   # Escrow contract interaction
│   │   └── services/          # API clients
│   │       ├── auth.js
│   │       ├── feed.js
│   │       └── notifications.js
│   └── package.json           # Node dependencies
│
├── contracts/                 # Smart Contracts
│   └── campus-contracts/
│       ├── smart_contracts/
│       │   ├── escrow/        # Milestone-based escrow
│       │   │   └── contract.py
│       │   └── hustle_score/  # Reputation NFTs
│       │       └── contract.py
│       ├── scripts/           # Deployment scripts
│       │   ├── demo_escrow.py
│       │   └── demo_hustle_score.py
│       └── simple_deploy.py   # Simple deployment helper
│
├── DEMO_GUIDE.md             # How to demo the platform
├── DEPLOYMENT.md             # Smart contract deployment guide
├── OAUTH_SETUP.md            # OAuth configuration guide
└── README.md                 # This file
```

---

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## Team Amateur
- **Aditya Gavane** - Backend & Blockchain Architecture 
-
