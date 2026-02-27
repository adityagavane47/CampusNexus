import algosdk

def generate_account():
    private_key, address = algosdk.account.generate_account()
    mnemonic = algosdk.mnemonic.from_private_key(private_key)
    print(f"Address: {address}")
    print(f"Mnemonic: {mnemonic}")
    
    with open(".env.testnet", "w") as f:
        f.write(f"DEPLOYER_MNEMONIC=\"{mnemonic}\"\n")
    print("Saved mnemonic to .env.testnet")

if __name__ == "__main__":
    generate_account()
