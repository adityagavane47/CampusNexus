/**
 * CampusNexus - useEscrow Hook
 * React hook for interacting with the Milestone Escrow contract
 */
import { useState, useCallback } from 'react';
import algosdk from 'algosdk';

import {
    deployEscrowContract,
    fundEscrowTransaction,
    releasePaymentTransaction,
    getAlgodClient
} from '../services/algorand';

export function useEscrow() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Create and Fund a new escrow for a project
     * Two-step process: 1. Deploy Contract, 2. Fund Contract
     */
    const createEscrow = useCallback(async (accountAddress, signer, freelancerAddress, totalAmountAlgo, numMilestones = 1) => {
        if (!accountAddress || !signer) {
            setError('Wallet not connected or signer missing');
            return null;
        }

        setIsLoading(true);
        setError(null);

        try {
            // STEP 1: Deploy Escrow Contract
            console.log('Step 1: Deploying Escrow Contract...');
            const deployTxn = await deployEscrowContract(
                accountAddress,
                freelancerAddress,
                numMilestones,
                totalAmountAlgo
            );

            // Sign deployment
            const signedDeployTxn = await signer([deployTxn]);

            // Send deployment
            const client = getAlgodClient();
            const { txId: deployTxId } = await client.sendRawTransaction(signedDeployTxn).do();

            // Wait for confirmation
            const deployResult = await algosdk.waitForConfirmation(client, deployTxId, 4);
            const appId = deployResult['application-index'];
            console.log(`Escrow Contract Deployed! App ID: ${appId}`);

            // STEP 2: Fund Escrow Contract
            console.log('Step 2: Funding Escrow Contract...');
            const fundTxns = await fundEscrowTransaction(
                accountAddress,
                appId,
                totalAmountAlgo
            );

            // Sign funding
            const signedFundTxns = await signer(fundTxns);

            // Send funding
            const { txId: fundTxId } = await client.sendRawTransaction(signedFundTxns).do();

            // Wait for confirmation
            await algosdk.waitForConfirmation(client, fundTxId, 4);
            console.log('Escrow Contract Funded!');

            return { applicationIndex: appId };

        } catch (err) {
            console.error('Create escrow error:', err);
            // Handle specific network mismatch error friendlier?
            const msg = err.message || 'Failed to create escrow';
            setError(msg);
            return null;
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Fund an existing escrow
     */
    const fundEscrow = useCallback(async (accountAddress, signer, escrowAppId, amountAlgo) => {
        if (!accountAddress || !signer) {
            setError('Wallet not connected');
            return null;
        }

        setIsLoading(true);
        setError(null);

        try {
            const txn = await fundEscrowTransaction(
                accountAddress,
                escrowAppId,
                amountAlgo
            );

            const signedTxn = await signer(txn);
            const client = getAlgodClient();
            const { txId } = await client.sendRawTransaction(signedTxn).do();
            const result = await algosdk.waitForConfirmation(client, txId, 4);

            console.log('Escrow funded:', result);
            return result;
        } catch (err) {
            console.error('Fund escrow error:', err);
            setError(err.message || 'Failed to fund escrow');
            return null;
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Release payment to freelancer
     */
    const releasePayment = useCallback(async (accountAddress, signer, escrowAppId, amountAlgo) => {
        if (!accountAddress || !signer) {
            setError('Wallet not connected');
            return null;
        }

        setIsLoading(true);
        setError(null);

        try {
            const txn = await releasePaymentTransaction(
                accountAddress,
                escrowAppId,
                amountAlgo
            );

            const signedTxn = await signer(txn);
            const client = getAlgodClient();
            const { txId } = await client.sendRawTransaction(signedTxn).do();
            const result = await algosdk.waitForConfirmation(client, txId, 4);

            console.log('Payment released:', result);
            return result;
        } catch (err) {
            console.error('Release payment error:', err);
            setError(err.message || 'Failed to release payment');
            return null;
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        createEscrow,
        fundEscrow,
        releasePayment,
        isLoading,
        error,
    };
}

export default useEscrow;
