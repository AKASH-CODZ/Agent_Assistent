#!/usr/bin/env python3
"""
Comprehensive Test Suite for Akash AI Backend API.
Tests all endpoints, validates responses, and checks system health.
"""

import requests
import json
import sys
from typing import Dict, Any, List
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class TestResult:
    """Test result container."""
    def __init__(self, name: str, passed: bool, message: str = "", data: Dict = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.data = data or {}
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} - {self.name}: {self.message}"

def test_health_check() -> TestResult:
    """Test the root health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return TestResult(
                "Root Health Check",
                True,
                f"Server running (v{data.get('version', 'unknown')})",
                data
            )
        else:
            return TestResult("Root Health Check", False, f"Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        return TestResult("Root Health Check", False, "Could not connect to server")
    except Exception as e:
        return TestResult("Root Health Check", False, str(e))

def test_api_health() -> TestResult:
    """Test the API health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return TestResult(
                "API v1 Health Check",
                True,
                "API endpoint responsive",
                data
            )
        else:
            return TestResult("API v1 Health Check", False, f"Status code: {response.status_code}")
    except Exception as e:
        return TestResult("API v1 Health Check", False, str(e))

def test_chat_endpoint(message: str, user_type: str = "visitor") -> TestResult:
    """Test the chat endpoint with different user types."""
    try:
        payload = {
            "message": message,
            "user_type": user_type
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            has_reply = "reply" in data and len(data["reply"]) > 0
            has_context = "context_used" in data
            
            return TestResult(
                f"Chat ({user_type})",
                has_reply and has_context,
                f"Reply received ({len(data['reply'])} chars), Context: {len(data.get('context_used', []))} items",
                data
            )
        else:
            return TestResult(f"Chat ({user_type})", False, f"Status: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        return TestResult(f"Chat ({user_type})", False, str(e))

def test_validation_error() -> TestResult:
    """Test that validation errors are handled properly."""
    try:
        # Send invalid payload (missing required fields)
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            headers={"Content-Type": "application/json"},
            json={},
            timeout=5
        )
        
        # Should return 422 Unprocessable Entity
        if response.status_code == 422:
            return TestResult("Validation Error Handling", True, "Properly rejects invalid input")
        else:
            return TestResult("Validation Error Handling", False, f"Expected 422, got {response.status_code}")
    except Exception as e:
        return TestResult("Validation Error Handling", False, str(e))

def test_response_time() -> TestResult:
    """Test API response time."""
    try:
        start_time = datetime.now()
        response = requests.get(f"{BASE_URL}/", timeout=5)
        end_time = datetime.now()
        
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        
        if response.status_code == 200:
            is_acceptable = response_time_ms < 2000  # < 2 seconds
            return TestResult(
                "Response Time",
                is_acceptable,
                f"{response_time_ms:.0f}ms {'(acceptable)' if is_acceptable else '(too slow)'}",
                {"response_time_ms": response_time_ms}
            )
        else:
            return TestResult("Response Time", False, f"Status code: {response.status_code}")
    except Exception as e:
        return TestResult("Response Time", False, str(e))

def run_all_tests() -> List[TestResult]:
    """Run all tests and return results."""
    print("\n🧪 Running Akash AI Backend Test Suite")
    print("=" * 60)
    
    results = []
    
    # Basic health checks
    print("\n1️⃣  Health Checks...")
    results.append(test_health_check())
    results.append(test_api_health())
    results.append(test_response_time())
    
    # Chat functionality tests
    print("\n2️⃣  Chat Functionality Tests...")
    test_cases = [
        ("Tell me about your projects", "visitor"),
        ("What technologies do you know?", "recruiter"),
        ("Show me your code examples", "developer"),
        ("Explain machine learning", "student"),
    ]
    
    for message, user_type in test_cases:
        result = test_chat_endpoint(message, user_type)
        results.append(result)
    
    # Validation tests
    print("\n3️⃣  Validation Tests...")
    results.append(test_validation_error())
    
    return results

def print_summary(results: List[TestResult]):
    """Print test summary."""
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    
    for result in results:
        print(result)
    
    print("\n" + "-" * 60)
    print(f"Total: {len(results)} tests | ✅ Passed: {passed} | ❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Check the server logs for details.")
        print("Make sure the server is running: uvicorn main:app --reload")
    else:
        print("\n🎉 All tests passed!")
    
    print("=" * 60)

def main():
    """Main test runner."""
    try:
        results = run_all_tests()
        print_summary(results)
        
        # Exit with error code if any tests failed
        failed = sum(1 for r in results if not r.passed)
        sys.exit(1 if failed > 0 else 0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {str(e)}")
        print("Make sure the server is running and accessible.")
        sys.exit(1)

if __name__ == "__main__":
    main()
