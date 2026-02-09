"""
Test script for the mock escrow implementation
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/escrow"

def test_create_escrow():
    """Test creating a new escrow"""
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
        print(f"✅ Escrow created successfully!")
        print(f"   Escrow ID: {result['id']}")
        print(f"   Status: {result['status']}")
        print(f"   Total Amount: {result['total_amount_algo']} ALGO")
        print(f"   Milestones: {len(result['milestones'])}")
        return result['id']
    else:
        print(f"❌ Failed to create escrow: {response.status_code}")
        print(response.text)
        return None

def test_get_escrow(escrow_id):
    """Test retrieving escrow details"""
    print(f"\n=== TEST 2: Get Escrow {escrow_id} ===")
    
    response = requests.get(f"{BASE_URL}/{escrow_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Escrow retrieved successfully!")
        print(f"   Client: {result['client_address']}")
        print(f"   Freelancer: {result['freelancer_address']}")
        print(f"   Status: {result['status']}")
        print(f"   Created: {result['created_at']}")
        return result
    else:
        print(f"❌ Failed to get escrow: {response.status_code}")
        return None

def test_complete_milestone(escrow_id, milestone_index):
    """Test marking a milestone as complete"""
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
        print(f"✅ Milestone marked as complete!")
        print(f"   Message: {result['message']}")
        print(f"   Milestone Status: {result['milestone']['status']}")
        return True
    else:
        print(f"❌ Failed to complete milestone: {response.status_code}")
        print(response.text)
        return False

def test_approve_milestone(escrow_id, milestone_index):
    """Test approving a milestone and releasing funds"""
    print(f"\n=== TEST 4: Approve Milestone {milestone_index} ===")
    
    params = {
        "client_address": "CLIENT_WALLET_ADDRESS_123"
    }
    
    response = requests.post(
        f"{BASE_URL}/{escrow_id}/milestone/{milestone_index}/approve",
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Milestone approved and funds released!")
        print(f"   Message: {result['message']}")
        print(f"   Milestone Status: {result['milestone']['status']}")
        return True
    else:
        print(f"❌ Failed to approve milestone: {response.status_code}")
        print(response.text)
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("TESTING MOCK ESCROW IMPLEMENTATION")
    print("=" * 50)
    
    # Test 1: Create escrow
    escrow_id = test_create_escrow()
    if not escrow_id:
        print("\n❌ Cannot proceed with tests - escrow creation failed")
        return
    
    # Test 2: Get escrow details
    test_get_escrow(escrow_id)
    
    # Test 3: Complete first milestone
    if test_complete_milestone(escrow_id, 0):
        # Test 4: Approve first milestone
        test_approve_milestone(escrow_id, 0)
    
    # Test 5: Complete second milestone
    if test_complete_milestone(escrow_id, 1):
        # Test 6: Approve second milestone
        test_approve_milestone(escrow_id, 1)
    
    # Final check: Get updated escrow
    print("\n=== FINAL CHECK: Get Updated Escrow ===")
    final_escrow = test_get_escrow(escrow_id)
    if final_escrow:
        print(f"\n📊 SUMMARY:")
        print(f"   Total Milestones: {len(final_escrow['milestones'])}")
        approved_count = sum(1 for m in final_escrow['milestones'] if m['status'] == 'approved')
        print(f"   Approved Milestones: {approved_count}")
        print(f"   Escrow Status: {final_escrow['status']}")
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()
