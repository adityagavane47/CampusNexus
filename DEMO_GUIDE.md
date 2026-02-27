# CampusNexus Smart Contract Demo Guide

This guide provides a structured way to demonstrate the core blockchain features of CampusNexus to judges.

## 🎯 Demo Objectives
1.  **Showcase Trustless Escrow**: Demonstrate how funds are locked and only released upon milestone completion.
2.  **Showcase Soulbound Reputation**: Demonstrate "Hustle Score" (SBT) minting and score updates.

## 🛠️ Prerequisites
- **Python 3.10+** installed
- **Algorand TestNet Account** with ALGO (for the deployer)
- `.env` file in `backend/` or `contracts/campus-contracts/` with `DEPLOYER_MNEMONIC`

## 🎬 1. Hustle Score (SBT) Demo
*The "Hustle Score" is a non-transferable token that tracks student reputation.*

### What to Say:
> "We built a Soulbound Token (SBT) on Algorand to track student reputation. This score is immutable, non-transferable, and lives on-chain, proving a student's actual contribution history."

### Live Action:
Run the demo script to mint a token and update a score live.

```bash
cd contracts/campus-contracts
python scripts/demo_hustle_score.py
```

### What they will see:
1.  **Deployment**: A new HustleScore contract is deployed.
2.  **Minting**: A student account is initialized (Minted).
3.  **Score Update**: The admin adds reputation points.
4.  **Verification**: The script reads the box storage to confirm the score is now `10`.

---

## 🤝 2. Milestone Escrow Demo
*The Escrow contract ensures freelancers get paid only when work is approved.*

### What to Say:
> "Our Escrow contract protects both parties. The client funds the contract, but money is only released when milestones are approved. This removes the need for a middleman."

### Live Action:
Run the escrow lifecycle simulation.

```bash
cd contracts/campus-contracts
python scripts/demo_escrow.py
```

### What they will see:
1.  **Creation**: An escrow contract is created for a freelancer.
2.  **Funding**: The client sends 1.2 ALGO to the contract (1.0 Payment + 0.2 Fees).
3.  **Release**: The client approves the work, and the contract automatically transfers funds to the freelancer.

---

## 🔍 Code Highlights (If Judges Ask)
Open these files to show the code:

- **Escrow Logic**: `contracts/escrow/milestone_escrow.py`
    - Show `approve_milestone` / `release_payment` checks.
    - Show `only_client` assertions.

- **SBT Logic**: `contracts/campus-contracts/smart_contracts/hustle_score/contract.py`
    - Show `scores = BoxMap(Account, UInt64)`.
    - Show "No transfer method" (enforcing Soulbound nature).
