/**
 * CampusNexus - useEscrow Hook
 * React hook for interacting with the Milestone Escrow contract
 */
import { useState, useCallback } from 'react';
import algosdk from 'algosdk';

import {
    createEscrowTransaction,
    fundEscrowTransaction,
    releasePaymentTransaction,
    getAlgodClient
} from '../services/algorand';

export function useEscrow() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Create a new escrow for a project
     */
    const createEscrow = useCallback(async (accountAddress, signer, freelancerAddress, totalAmountAlgo, numMilestones = 1) => {
        if (!accountAddress || !signer) {
            setError('Wallet not connected or signer missing');
            return null;
        }

        setIsLoading(true);
        setError(null);

        try {
            const txn = await createEscrowTransaction(
                accountAddress,
                freelancerAddress,
                numMilestones,
                totalAmountAlgo
            );

            // Sign with Pera Wallet
            const signedTxn = await signer(txn);

            // Submit transaction
            const client = getAlgodClient();
            const { txId } = await client.sendRawTransaction(signedTxn).do();

            // Wait for confirmation
            const result = await algosdk.waitForConfirmation(client, txId, 4);

            console.log('Escrow created:', result);
            return result;
        } catch (err) {
            console.error('Create escrow error:', err);
            setError(err.message || 'Failed to create escrow');
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
