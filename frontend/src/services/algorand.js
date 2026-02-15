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
    escrow: 755290189,        // MilestoneEscrow App ID
    hustleScore: 755519723,   // HustleScore App ID
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
        return Number(accountInfo.amount) / 1_000_000; // Convert microAlgos to ALGO
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
    console.log('[Escrow] createEscrowTransaction called with:', {
        clientAddress,
        freelancerAddress,
        numMilestones,
        totalAmountAlgo
    });

    // Validate client address
    if (!clientAddress) {
        throw new Error('Client address must not be null or undefined');
    }

    // Use client address as placeholder if freelancer not specified
    const freelancer = freelancerAddress || clientAddress;
    console.log('[Escrow] Using freelancer address:', freelancer);

    const client = getAlgodClient();
    console.log('[Escrow] Got algod client, fetching params...');

    const params = await client.getTransactionParams().do();
    console.log('[Escrow] Got suggested params:', params);

    console.log('[Escrow] Decoding freelancer address...');
    const decodedFreelancer = algosdk.decodeAddress(freelancer);
    console.log('[Escrow] Decoded freelancer OK');

    console.log('[Escrow] Encoding numMilestones:', numMilestones);
    const encodedMilestones = algosdk.encodeUint64(numMilestones);
    console.log('[Escrow] Encoded milestones OK');

    // Application call to create escrow
    const appArgs = [
        new TextEncoder().encode('create_escrow'),
        decodedFreelancer.publicKey,
        encodedMilestones,
        new TextEncoder().encode('[]'),
    ];

    console.log('[Escrow] Building transaction with appIndex:', CONTRACT_IDS.escrow);
    console.log('[Escrow] from address:', clientAddress);

    const txn = algosdk.makeApplicationCallTxnFromObject({
        from: clientAddress,
        suggestedParams: params,
        appIndex: CONTRACT_IDS.escrow,
        appArgs: appArgs,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
    });

    console.log('[Escrow] Transaction created successfully');
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
    const appArgs = [new TextEncoder().encode('fund_escrow')];
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
        new TextEncoder().encode('complete_milestone'),
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
        new TextEncoder().encode('approve_milestone'),
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

// Import TEAL programs
import { APPROVAL_PROGRAM, CLEAR_PROGRAM } from '../contracts/escrow';

/**
 * Compile TEAL program
 */
async function compileProgram(client, programSource) {
    const encoder = new TextEncoder();
    const programBytes = encoder.encode(programSource);
    const compileResponse = await client.compile(programBytes).do();
    // Browser-compatible Base64 decode
    const binaryString = atob(compileResponse.result);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}

/**
 * Deploy a new Escrow Contract
 */
export async function deployEscrowContract(
    clientAddress,
    freelancerAddress,
    numMilestones,
    totalAmountAlgo
) {
    console.log('[Escrow] deployEscrowContract called with:', {
        client: clientAddress,
        freelancer: freelancerAddress,
        milestones: numMilestones,
        amount: totalAmountAlgo
    });

    if (!clientAddress) {
        throw new Error('deployEscrowContract: clientAddress is missing');
    }
    const cleanClientAddress = clientAddress.trim();
    if (!algosdk.isValidAddress(cleanClientAddress)) {
        throw new Error(`deployEscrowContract: Invalid client address: "${cleanClientAddress}"`);
    }

    const client = getAlgodClient();
    const params = await client.getTransactionParams().do();

    // Compile programs
    let approvalProgram, clearProgram;
    try {
        console.log('[Escrow] Compiling approval program...');
        approvalProgram = await compileProgram(client, APPROVAL_PROGRAM);
        console.log('[Escrow] Compiling clear program...');
        clearProgram = await compileProgram(client, CLEAR_PROGRAM);
    } catch (e) {
        throw new Error(`Compilation failed: ${e.message}`);
    }

    // Prepare arguments
    const selector = new Uint8Array([0xab, 0x65, 0x04, 0x4f]);
    const decodedFreelancer = algosdk.decodeAddress(freelancerAddress || cleanClientAddress);
    const encodedMilestones = algosdk.encodeUint64(numMilestones);

    const appArgs = [
        selector,
        decodedFreelancer.publicKey,
        encodedMilestones
    ];

    console.log('[Escrow] Creating ApplicationCreate transaction...');

    const txn = algosdk.makeApplicationCreateTxnFromObject({
        from: cleanClientAddress,
        sender: cleanClientAddress, // Required for algosdk v3
        suggestedParams: params,
        onComplete: algosdk.OnApplicationComplete.NoOpOC,
        approvalProgram: approvalProgram,
        clearProgram: clearProgram,
        numLocalInts: 0,
        numLocalByteSlices: 0,
        numGlobalInts: 4,
        numGlobalByteSlices: 4,
        appArgs: appArgs,
        accounts: [],
        foreignApps: [],
        foreignAssets: [],
        boxes: [],
        note: new Uint8Array(0)
    });

    return txn;

    return txn;
}
