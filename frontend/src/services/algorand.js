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

// Current network - change this for deployment
const CURRENT_NETWORK = 'testnet';

// Contract App IDs - Deployed on Testnet (2026-02-10)
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
 * Create escrow transaction
 */
export async function createEscrowTransaction(
    senderAddress,
    freelancerAddress,
    amountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    // Application call to create escrow
    const appArgs = [
        new TextEncoder().encode('create_escrow'),
        algosdk.decodeAddress(freelancerAddress).publicKey,
        algosdk.encodeUint64(amountAlgo * 1_000_000),
    ];

    const txn = algosdk.makeApplicationCallTxnFromObject({
        from: senderAddress,
        suggestedParams: params,
        appIndex: CONTRACT_IDS.escrow,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    return txn;
}

/**
 * Fund escrow transaction
 */
export async function fundEscrowTransaction(
    senderAddress,
    escrowAppId,
    amountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    // Payment to escrow app
    const escrowAddress = algosdk.getApplicationAddress(escrowAppId);

    const paymentTxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        from: senderAddress,
        to: escrowAddress,
        amount: amountAlgo * 1_000_000,
        suggestedParams: params,
    });

    return paymentTxn;
}

/**
 * Release payment from escrow
 */
export async function releasePaymentTransaction(
    clientAddress,
    escrowAppId,
    amountAlgo
) {
    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    const appArgs = [
        new TextEncoder().encode('release_payment'),
        algosdk.encodeUint64(amountAlgo * 1_000_000),
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
    releasePaymentTransaction,
    getCurrentNetwork,
    formatAlgo,
    CONTRACT_IDS,
};
