# CampusNexus - Smart Contract Deployment Guide

This guide explains how to deploy the Algorand smart contracts to a real blockchain network (Localnet or Testnet) instead of using the mock backend.

## Current Status

✅ Smart contracts written (`contracts/campus-contracts/smart_contracts/escrow/contract.py`)
✅ Frontend integration ready (`frontend/src/services/algorand.js`, `frontend/src/hooks/useEscrow.js`)
✅ Mock backend functional for development (`backend/app/routers/escrow.py`)

## Prerequisites

### Windows Users

Install **Visual Studio Build Tools** (required for `coincurve` cryptography library):

1. Download: [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Run installer and select "Desktop development with C++"
3. After installation, restart your terminal

### Linux/Mac Users

Install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

# macOS
xcode-select --install
```

### All Platforms

- Docker Desktop (for Localnet)
- AlgoKit CLI (already installed)
- Poetry (already installed)

## Deployment Steps

### Option 1: Deploy to Localnet (Recommended for Testing)

Localnet is a local Algorand blockchain running in Docker. It's perfect for development and testing.

1. **Start Localnet**:
   ```bash
   cd contracts/campus-contracts
   algokit localnet start
   ```

2. **Install Dependencies**:
   ```bash
   poetry install
   ```

3. **Build Contracts**:
   ```bash
   algokit project run build
   ```

4. **Deploy to Localnet**:
   ```bash
   algokit project deploy localnet
   ```

5. **Note the App ID**: After deployment, you'll see output like:
   ```
   Deployed MilestoneEscrow with app_id: 1001
   ```

6. **Update Frontend Configuration**:
   Edit `frontend/src/services/algorand.js`:
   ```javascript
   const CURRENT_NETWORK = 'localnet';  // Change from 'testnet'
   
   export const CONTRACT_IDS = {
       escrow: 1001,  // Use the App ID from deployment
       hustleScore: 0,
   };
   ```

### Option 2: Deploy to Testnet (For Public Demo)

Testnet is Algorand's public test network. Use this when you want others to interact with your app.

1. **Generate Environment File**:
   ```bash
   cd contracts/campus-contracts
   algokit generate env-file -a target_network testnet
   ```

2. **Create Deployer Account**:
   ```bash
   poetry run python generate_funding_account.py
   ```
   This creates `.env.testnet` with your mnemonic.

3. **Fund the Account**:
   - Copy the address from the output
   - Go to [Algorand Testnet Dispenser](https://bank.testnet.algorand.network/)
   - Paste the address and click "Dispense"

4. **Build & Deploy**:
   ```bash
   algokit project run build
   algokit project deploy testnet
   ```

5. **Update Frontend**:
   ```javascript
   const CURRENT_NETWORK = 'testnet';
   
   export const CONTRACT_IDS = {
       escrow: YOUR_APP_ID_HERE,  // From deployment output
       hustleScore: 0,
   };
   ```

## Switching from Mock to Real Blockchain

After deploying, you need to update the backend to use the real smart contracts instead of the mock:

### Backend Changes

Edit `backend/app/routers/escrow.py`:

1. **Remove** the in-memory database:
   ```python
   # DELETE THIS:
   escrows_db: list[dict] = []
   ```

2. **Add** AlgoKit Utils imports:
   ```python
   from algokit_utils import get_algod_client
   from algosdk import transaction
   ```

3. **Update** the `create_escrow` function to call the smart contract instead of storing in memory.

> **Note**: Full blockchain integration requires significant backend refactoring. For hackathons, the mock is recommended.

## Testing Your Deployment

### Test with AlgoKit Explorer

```bash
algokit explore
```

This opens a web UI where you can:
- View your deployed contracts
- Inspect transactions
- Test contract methods

### Test from Frontend

1. Connect your Pera Wallet (make sure it's on the same network: Localnet/Testnet)
2. Create a project
3. Use the escrow features
4. Check the blockchain explorer to see the transactions

## Troubleshooting

### `coincurve` Build Errors (Windows)

**Error**: `ModuleNotFoundError: No module named 'dotenv'` or build failures

**Solution**: Install Visual Studio Build Tools (see Prerequisites)

### Docker Not Running

**Error**: `Container engine isn't running`

**Solution**: Start Docker Desktop before running `algokit localnet start`

### Out of Funds on Testnet

**Solution**: 
- Use the dispenser: https://bank.testnet.algorand.network/
- Each request gives you 10 ALGO (enough for ~100 transactions)

## Production Deployment (Mainnet)

⚠️ **WARNING**: Mainnet uses real ALGO with real value. Only deploy when ready.

1. Change network to `mainnet` in `algorand.js`
2. Fund your deployer account with real ALGO
3. Deploy: `algokit project deploy mainnet`
4. Test thoroughly before announcing

## Additional Resources

- [AlgoKit Documentation](https://github.com/algorandfoundation/algokit-cli)
- [Algorand Developer Portal](https://developer.algorand.org/)
- [Pera Wallet Documentation](https://perawallet.app/)
