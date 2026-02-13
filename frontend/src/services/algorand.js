/**
 * CampusNexus - Algorand Service
 * Handles all blockchain interactions from the frontend
 */
import algosdk from 'algosdk';

// Network Configuration
const NETWORKS = {
    localnet: {
        algodServer: 'http://localhost',
        algodPort: 4001,
        algodToken: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        indexerServer: 'http://localhost',
        indexerPort: 8980,
    },
    testnet: {
        algodServer: 'https://testnet-api.algonode.cloud',
        algodPort: 443,
        algodToken: '',
        indexerServer: 'https://testnet-idx.algonode.cloud',
        indexerPort: 443,
    },
    mainnet: {
        algodServer: 'https://mainnet-api.algonode.cloud',
        algodPort: 443,
        algodToken: '',
        indexerServer: 'https://mainnet-idx.algonode.cloud',
        indexerPort: 443,
    },
};

// Current network - TestNet has working deployed contracts
const CURRENT_NETWORK = 'testnet';

// Contract App IDs - Deployed on Testnet (previously deployed, working)
export const CONTRACT_IDS = {
    escrow: 755290899,        // MilestoneEscrow App ID
    hustleScore: 755290900,   // HustleScore App ID
};

/**
 * Get Algod client for current network
 */
export function getAlgodClient() {
    const network = NETWORKS[CURRENT_NETWORK];
    return new algosdk.Algodv2(
        network.algodToken,
        network.algodServer,
        network.algodPort
    );
}

/**
 * Get suggested transaction parameters
 */
export async function getSuggestedParams() {
    const client = getAlgodClient();
    return await client.getTransactionParams().do();
}

/**
 * Get account balance in ALGO
 */
export async function getAccountBalance(address) {
    try {
        const client = getAlgodClient();
        const accountInfo = await client.accountInformation(address).do();
        return accountInfo.amount / 1_000_000; // Convert microAlgos to ALGO
    } catch (error) {
        console.error('Error fetching balance:', error);
        return 0;
    }
}

/**
 * Create escrow transaction with milestone support
 */
export async function createEscrowTransaction(
    clientAddress,
    freelancerAddress,
    numMilestones,
    totalAmountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    // Application call to create escrow
    const appArgs = [
        new Uint8Array(Buffer.from('create_escrow')),
        algosdk.decodeAddress(freelancerAddress).publicKey,
        algosdk.encodeUint64(numMilestones),
        new Uint8Array(Buffer.from('[]')),  // Milestone amounts placeholder
    ];

    const txn = algosdk.makeApplicationCallTxnFromObject({
        from: clientAddress,
        suggestedParams: params,
        appIndex: CONTRACT_IDS.escrow,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    return txn;
}

/**
 * Fund escrow transaction (Atomic Transfer: Payment + App Call)
 */
export async function fundEscrowTransaction(
    clientAddress,
    escrowAppId,
    amountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    // Get escrow app address
    const appAddress = algosdk.getApplicationAddress(escrowAppId);

    // Transaction 1: Payment to escrow app
    const payTxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        from: clientAddress,
        to: appAddress,
        amount: amountAlgo * 1_000_000,  // Convert ALGO to microALGOs
        suggestedParams: params,
    });

    // Transaction 2: App call to fund_escrow
    const appArgs = [new Uint8Array(Buffer.from('fund_escrow'))];
    const appTxn = algosdk.makeApplicationCallTxnFromObject({
        from: clientAddress,
        suggestedParams: params,
        appIndex: escrowAppId,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    // Group transactions for atomic execution
    const txns = [payTxn, appTxn];
    algosdk.assignGroupID(txns);

    return txns;  // Returns array for Pera Wallet signing
}

/**
 * Complete milestone transaction (freelancer marks work complete)
 */
export async function completeMilestoneTransaction(
    freelancerAddress,
    escrowAppId,
    milestoneIndex
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    const appArgs = [
        new Uint8Array(Buffer.from('complete_milestone')),
        algosdk.encodeUint64(milestoneIndex),
    ];

    const txn = algosdk.makeApplicationCallTxnFromObject({
        from: freelancerAddress,
        suggestedParams: params,
        appIndex: escrowAppId,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    return txn;
}

/**
 * Approve milestone and release payment (client approves freelancer's work)
 */
export async function approveMilestoneTransaction(
    clientAddress,
    escrowAppId,
    milestoneIndex,
    amountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    const appArgs = [
        new Uint8Array(Buffer.from('approve_milestone')),
        algosdk.encodeUint64(milestoneIndex),
        algosdk.encodeUint64(amountAlgo * 1_000_000),  // Convert to microALGOs
    ];

    const txn = algosdk.makeApplicationCallTxnFromObject({
        from: clientAddress,
        suggestedParams: params,
        appIndex: escrowAppId,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    return txn;
}

/**
 * Legacy: Release payment transaction (deprecated - use approveMilestoneTransaction)
 */
export async function releasePaymentTransaction(clientAddress, escrowAppId, amountAlgo) {
    return approveMilestoneTransaction(clientAddress, escrowAppId, 0, amountAlgo);
}

/**
 * Get current network name
 */
export function getCurrentNetwork() {
    return CURRENT_NETWORK;
}

/**
 * Format ALGO amount
 */
export function formatAlgo(microAlgos) {
    return (microAlgos / 1_000_000).toFixed(2);
}

export default {
    getAlgodClient,
    getSuggestedParams,
    getAccountBalance,
    createEscrowTransaction,
    fundEscrowTransaction,
    completeMilestoneTransaction,
    approveMilestoneTransaction,
    releasePaymentTransaction,
    getCurrentNetwork,
    formatAlgo,
    CONTRACT_IDS,
};
