import sys
import os

sys.path.append(os.getcwd())

try:
    import smart_contracts.artifacts.escrow.milestone_escrow_client as escrow_module
    print("Escrow module classes:")
    for name in dir(escrow_module):
        if "Client" in name:
            print(f"- {name}")

    import smart_contracts.artifacts.hustle_score.hustle_score_client as hustle_module
    print("\nHustleScore module classes:")
    for name in dir(hustle_module):
        if "Client" in name:
            print(f"- {name}")
            
except Exception as e:
    print(f"Error: {e}")
