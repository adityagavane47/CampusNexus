import requests
import json

BASE_URL = "http://localhost:8000/api/escrow"

def test_create_escrow():

    print("\n=== TEST 1: Create Escrow ===")
    
    escrow_data = {
        "project_id": 1,
        "client_address": "CLIENT_WALLET_ADDRESS_123",
        "freelancer_address": "FREELANCER_WALLET_ADDRESS_456",
        "total_amount_algo": 100.0,
        "milestones": [
            {
                "title": "Design Phase",
                "description": "Complete UI/UX designs",
                "amount_algo": 30.0
            },
            {
                "title": "Development Phase",
                "description": "Implement frontend and backend",
                "amount_algo": 50.0
            },
            {
                "title": "Testing Phase",
                "description": "Test and deploy",
                "amount_algo": 20.0
            }
        ]
    }
    
    response = requests.post(BASE_URL, json=escrow_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Escrow metadata created successfully!")
        print(f"   Message: {result.get('message')}")
        if 'contract_params' in result:
             print(f"   Contract Params: Present")
        
        TEST_APP_ID = 755290189 
        print(f"   Using existing App ID for tests: {TEST_APP_ID}")
        return TEST_APP_ID
    else:
        print(f"❌ Failed to create escrow: {response.status_code}")
        print(response.text)
        return None

def test_get_escrow(escrow_id):

    print(f"\n=== TEST 2: Get Escrow {escrow_id} ===")
    
    response = requests.get(f"{BASE_URL}/{escrow_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Escrow retrieved successfully from blockchain!")
        print(f"   Client: {result['client_address']}")
        print(f"   Freelancer: {result['freelancer_address']}")
        print(f"   Status: {result['status']}")
        return result
    else:
        print(f"❌ Failed to get escrow: {response.status_code}")
        print(response.text)
        return None

def test_complete_milestone(escrow_id, milestone_index):

    print(f"\n=== TEST 3: Complete Milestone {milestone_index} ===")
    
    params = {
        "freelancer_address": "FREELANCER_WALLET_ADDRESS_456"
    }
    
    response = requests.post(
        f"{BASE_URL}/{escrow_id}/milestone/{milestone_index}/complete",
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Milestone completion instruction received!")
        print(f"   Message: {result['message']}")
        print(f"   Tx Params: {result['params']}")
        return True
    else:
        print(f"❌ Failed to request milestone completion: {response.status_code}")
        print(response.text)
        return False

def test_approve_milestone(escrow_id, milestone_index):

    print(f"\n=== TEST 4: Approve Milestone {milestone_index} ===")
    
    params = {
        "client_address": "CLIENT_WALLET_ADDRESS_123",
         "amount_algo": 10.0
    }
    
    response = requests.post(
        f"{BASE_URL}/{escrow_id}/milestone/{milestone_index}/approve",
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Milestone approval instruction received!")
        print(f"   Message: {result['message']}")
        print(f"   Tx Params: {result['params']}")
        return True
    else:
        print(f"❌ Failed to request milestone approval: {response.status_code}")
        print(response.text)
        return False

def main():

    print("=" * 50)
    print("TESTING MOCK ESCROW IMPLEMENTATION")
    print("=" * 50)
    
    escrow_id = test_create_escrow()
    if not escrow_id:
        print("\n❌ Cannot proceed with tests - escrow creation failed")
        return
    
    test_get_escrow(escrow_id)
    
    if test_complete_milestone(escrow_id, 0):
        test_approve_milestone(escrow_id, 0)
    
    if test_complete_milestone(escrow_id, 1):
        test_approve_milestone(escrow_id, 1)
    
    print("\n=== FINAL CHECK: Get Updated Escrow ===")
    final_escrow = test_get_escrow(escrow_id)
    if final_escrow:
        print(f"\n📊 SUMMARY:")
        print(f"   Total Milestones: {final_escrow.get('num_milestones', 'N/A')}")
        print(f"   Completed Milestones: {final_escrow.get('completed_milestones', 'N/A')}")
        print(f"   Escrow Status: {final_escrow['status']}")
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
