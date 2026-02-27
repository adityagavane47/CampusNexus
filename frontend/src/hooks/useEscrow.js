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

    
    const createEscrow = useCallback(async (accountAddress, signer, freelancerAddress, totalAmountAlgo, numMilestones = 1) => {
        if (!accountAddress || !signer) {
            setError('Wallet not connected or signer missing');
            return null;
        }

        setIsLoading(true);
        setError(null);

        try {
            console.log('Step 1: Deploying Escrow Contract...');
            const deployTxn = await deployEscrowContract(
                accountAddress,
                freelancerAddress,
                numMilestones,
                totalAmountAlgo
            );

            const signedDeployTxn = await signer([deployTxn]);

            const client = getAlgodClient();
            const { txId: deployTxId } = await client.sendRawTransaction(signedDeployTxn).do();

            const deployResult = await algosdk.waitForConfirmation(client, deployTxId, 4);
            const appId = deployResult['application-index'];
            console.log(`Escrow Contract Deployed! App ID: ${appId}`);

            console.log('Step 2: Funding Escrow Contract...');
            const fundTxns = await fundEscrowTransaction(
                accountAddress,
                appId,
                totalAmountAlgo
            );

            const signedFundTxns = await signer(fundTxns);

            const { txId: fundTxId } = await client.sendRawTransaction(signedFundTxns).do();

            await algosdk.waitForConfirmation(client, fundTxId, 4);
            console.log('Escrow Contract Funded!');

            return { applicationIndex: appId };

        } catch (err) {
            console.error('Create escrow error:', err);
            const msg = err.message || 'Failed to create escrow';
            setError(msg);
            return null;
        } finally {
            setIsLoading(false);
        }
    }, []);

    
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
