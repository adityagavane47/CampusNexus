# 🎓 CampusNexus Walkthrough: The Student Creator Journey

Welcome to **CampusNexus**. This guide follows my journey—**Aravind**, a third-year CS student at VIT Pune—as I use this decentralized ecosystem to turn my idea into reality.

---

## 📖 Chapter 1: The Need

I have a brilliant idea for a **Web3-enabled IoT Weather Station**, but I’m facing two problems:
1.  I need a **teammate** who is an expert in Arduino hardware (I’m only good at Solidity).
2.  I need **5 ALGO** to buy a specific sensor from a senior.

I open **CampusNexus**, our campus decentralized app (dApp), to solve both problems without relying on trust-based IOUs or messy WhatsApp groups.

---

## 🔍 Chapter 2: The Discovery

I navigate to the **"Create Project"** section and post my refined idea:
> *"Building a decentralized weather station. Need an IoT expert to handle ESP32 wiring."*

Behind the scenes, the **AI Skill-Matcher** (`backend/app/services/ai_matching.py`) springs into action. It analyzes my project description using NLP and scans the student database.

-   **Input**: "IoT", "ESP32", "Wiring"
-   **Match Found**: *Sneha*, an Electronics student who listed "Embedded Systems" as a skill.

I receive a recommendation card for Sneha and invite her to the team.

---

## 🤝 Chapter 3: The Trust

Sneha agrees, but she wants assurance that she'll be paid for her hardware contribution. I propose using the **Milestone-Based Escrow**.

1.  **Initiation**: I set up a milestone: *"Complete Sensor Integration"*.
2.  **Locking Funds**: I attach a bounty of **5 ALGO**.
3.  **Signing**: I click "Deposit".

> **The Pera Wallet Experience**:
> A pop-up from **Pera Wallet** appears on my phone. I scan the QR code (or approve the notification). The smart contract (`contracts/campus-contracts/smart_contracts/escrow/contract.py`) verifies my signature and securely locks the 5 ALGO on the blockchain.

**Status**: 🔒 *Funds Locked in Smart Contract*

---

## 🏆 Chapter 4: The Reward

Two days later, Sneha finishes the wiring and uploads a video proof to the project feed.

1.  **Verification**: I review the work and click **"Approve Milestone"**.
2.  **Release**: The smart contract instantly releases the **5 ALGO** to Sneha's wallet. No middleman, no delays.
3.  **Reputation Mint**:
    *   Because our collaboration was successful, the **Hustle-Score** contract executes.
    *   An **SBT (Soulbound Token)** is minted to both my profile and Sneha's, permanently increasing our on-chain reputation.

**My Profile Update**:
*   **Hustle Score**: ⬆️ +10
*   **Trust Rating**: ★★★★★
*   **Portfolio**: "Web3 Weather Station" added (Verified)

---

## 🚀 Conclusion

Through CampusNexus, I didn't just find a teammate; I built a verifiable reputation and executed a trustless financial transaction.

**Ready to start your journey?**
[Connect your Wallet](#) and build the future.
