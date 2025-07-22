#!/usr/bin/env python3
"""
Simple test to verify PolitiQ application is working
"""

import requests
import time
import subprocess
import threading
import os
import sys

def start_server():
    """Start the FastAPI server in the background"""
    os.system("source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 > server.log 2>&1 &")

def test_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8002"
    
    print("🧪 Testing PolitiQ Application...")
    
    # Wait for server to start
    time.sleep(3)
    
    # Test API endpoints
    tests = [
        ("/", "Dashboard"),
        ("/api/districts", "Districts API"),
        ("/api/stats", "Statistics API"),
        ("/hierarchy", "Hierarchy Management"),
        ("/booths", "Booth Management"),
        ("/voters", "Voter Search"),
        ("/upload-logs", "Upload Logs"),
    ]
    
    passed = 0
    failed = 0
    
    for endpoint, description in tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: PASSED ({response.status_code})")
                passed += 1
            else:
                print(f"❌ {description}: FAILED ({response.status_code})")
                failed += 1
        except Exception as e:
            print(f"❌ {description}: ERROR ({str(e)})")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! PolitiQ application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    
    # Stop server
    os.system("pkill -f 'uvicorn.*8002'")

if __name__ == "__main__":
    print("🚀 Starting PolitiQ Test Suite...")
    start_server()
    test_endpoints()
    print("✅ Test completed!")